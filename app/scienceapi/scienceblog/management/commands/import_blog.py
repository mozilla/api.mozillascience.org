from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_text
from django.utils.html import linebreaks, strip_tags
from django.db import transaction

from collections import defaultdict
from datetime import datetime, timezone
import re
from time import mktime
from xml.dom.minidom import parse
from bs4 import BeautifulSoup
from xml.dom import Node

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from mezzanine.generic.models import Keyword, ThreadedComment
from mezzanine.utils.html import decode_entities

User = get_user_model()


class Command(BaseCommand):
    """
    This command:
    - Finds or creates authors using their email_address
    - Converts blog image paths from wordpress to settings.MEDIA_URL
    - Converts featured image paths to url relative to settings.MEDIA_URL
    - Imports blogs, categories, tags, comments, fetured images from wordpress.
    """

    help = 'Migrate blog from wordpress to mezzanine.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', action='store_false', dest='interactive',
            help='Do NOT prompt for input of any kind. '
                 'Fields will be truncated if too long.')
        parser.add_argument(
            '-u', '--url', dest='url', help='URL to wordpress export file')

    def __init__(self, **kwargs):
        self.posts = []
        super().__init__(**kwargs)

    def add_post(self, author, title=None, content=None, pub_date=None,
                 tags=None, categories=None, comments=None,
                 featured_image=None):
        """
        Adds a post to the post list for processing.
        - `title` and `content` are strings for the post.
        - `pub_date` is assumed to be a `datetime` object.
        - `tags` and `categories` are sequences of strings.
        - `comments` is a sequence of dicts - each dict should be the
          return value of `add_comment`.
        - `author` is a user object.
        - `featured_image` is a link to image.
        """
        if not title:
            title = strip_tags(content).split('. ')[0]
        title = decode_entities(title)
        if categories is None:
            categories = []
        if tags is None:
            tags = []
        if comments is None:
            comments = []

        self.posts.append({'title': force_text(title),
                           'publish_date': pub_date,
                           'content': force_text(content),
                           'categories': categories,
                           'tags': tags,
                           'comments': comments,
                           'user': author,
                           'featured_image': featured_image})

        return self.posts[-1]

    def add_comment(self, post=None, name=None, email=None, pub_date=None,
                    website=None, body=None):
        """
        Adds a comment to the post provided.
        """
        if post is None:
            if not self.posts:
                raise CommandError('Cannot add comments without posts')
            post = self.posts[-1]

        post['comments'].append({'user_name': name,
                                 'user_email': email,
                                 'submit_date': pub_date,
                                 'user_url': website,
                                 'comment': body})

    def trunc(self, model, prompt, **fields):
        """
        Truncates fields values for the given model. Prompts for a new
        value if truncation occurs.
        """
        for field_name, value in fields.items():
            if value is not None:
                field = model._meta.get_field(field_name)
                max_length = getattr(field, 'max_length', None)
                if not max_length:
                    continue
                elif not prompt:
                    fields[field_name] = value[:max_length]
                    continue
                while len(value) > max_length:
                    encoded_value = value.encode('utf-8')

                    new_value = input('The value for the field %s. %s '
                                      'exceeds its maximum length of %s '
                                      'chars: %s\n\n Enter a new value for '
                                      'it, or press return to have it '
                                      'truncated: ' %
                                      (model.__name__, field_name, max_length,
                                       encoded_value))

                    value = new_value if new_value else value[:max_length]
                fields[field_name] = value
        return fields

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Processes the converted data into the Mezzanine database correctly.
        """

        if options.get('url') is None:
            raise CommandError('Incorrect usage. See import_blog -h')

        site = Site.objects.get_current()
        verbosity = int(options.get('verbosity', 1))
        prompt = options.get('interactive')

        self.handle_import(options)

        for post_data in self.posts:
            categories = post_data.pop('categories')
            tags = post_data.pop('tags')
            comments = post_data.pop('comments')

            post_data = self.trunc(BlogPost, prompt, **post_data)

            initial = {
                'title': post_data.pop('title'),
                'user': post_data.pop('user')
            }

            if post_data['publish_date'] is None:
                post_data['status'] = CONTENT_STATUS_DRAFT
            post, created = BlogPost.objects.get_or_create(**initial)

            for k, v in post_data.items():
                setattr(post, k, v)
            post.save()

            if created and verbosity >= 1:
                print('Imported post: %s' % post)

            for name in categories:
                cat = self.trunc(BlogCategory, prompt, title=name)
                if not cat['title']:
                    continue
                cat, created = BlogCategory.objects.get_or_create(**cat)
                if created and verbosity >= 1:
                    print('Imported category: %s' % cat)
                post.categories.add(cat)

            for comment in comments:
                comment = self.trunc(ThreadedComment, prompt, **comment)
                comment['site'] = site
                post.comments.create(**comment)
                if verbosity >= 1:
                    print('Imported comment by: %s' % comment['user_name'])

            self.add_meta(post, tags, prompt, verbosity)

    def add_meta(self, post, tags, prompt, verbosity):
        """
        Adds tags for the given blog post.
        """
        for tag in tags:
            keyword = self.trunc(Keyword, prompt, title=tag)
            keyword, created = Keyword.objects.get_or_create_iexact(**keyword)
            post.keywords.create(keyword=keyword)
            if created and verbosity >= 1:
                print('Imported tag: %s' % keyword)

    def handle_import(self, options):
        """
        Gets the posts from either the provided URL or the path if it
        is local.
        """
        url = options.get('url')

        try:
            import feedparser
        except ImportError:
            raise CommandError('Could not import the feedparser library.')
        feed = feedparser.parse(url)

        # We also use xml minidom since some of the information we need
        # is not extracted by feedparser
        xml = parse(url)

        # Search for or create blog authors using their email address
        wp_authors = xml.getElementsByTagName('wp:author')
        users = {}
        for author in wp_authors:
            wp_login_id = self.get_text(author, 'wp:author_login')
            email = self.get_text(author, 'wp:author_email')
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = wp_login_id
                user.first_name = self.get_text(author, 'wp:author_first_name')
                user.last_name = self.get_text(author, 'wp:author_last_name')
                user.set_unusable_password()
                user.save()
            # This would be used when associating blogs to their user objects
            users[wp_login_id] = user

        xmlitems = xml.getElementsByTagName('item')

        # Get all attachments from the feed and store them in a dictionary with
        # attachment_id as key
        attachments = {}
        for entry in feed['entries']:
            if entry.wp_post_type == 'attachment':
                attachments[entry.wp_post_id] = self.correct_url(
                    entry.wp_attachment_url, return_rel=True)

        for (i, entry) in enumerate(feed['entries']):

            if entry.wp_post_type == 'post':
                # Get a pointer to the right position in the minidom as well.
                xmlitem = xmlitems[i]
                content = linebreaks(
                    self.wp_caption(entry.content[0]['value']))

                # Get the time struct of the published date if possible and
                # the updated date if we can't.
                pub_date = getattr(
                    entry, 'published_parsed', entry.updated_parsed)
                if pub_date:
                    pub_date = datetime.fromtimestamp(mktime(pub_date))
                    pub_date = pub_date.replace(tzinfo=timezone.utc)

                # Tags and categories are all under 'tags'
                # marked with a scheme.
                terms = defaultdict(set)
                for item in getattr(entry, 'tags', []):
                    terms[item.scheme].add(item.term)

                # Get all image tags from blog content and correct their src.
                content = BeautifulSoup(content, 'html.parser')
                images = content.find_all('img')
                for image in images:
                    image['src'] = self.correct_url(image['src'].strip())
                content = str(content)

                # Get attachment_id of featured image if present and get
                # corresponding image url
                featured_image = None
                for m in xmlitem.getElementsByTagName('wp:postmeta'):
                    if(self.get_text(m, 'wp:meta_key') == '_thumbnail_id'):
                        featured_image = attachments[self.get_text(
                            m, 'wp:meta_value')]

                post = self.add_post(title=entry.title, content=content,
                                     pub_date=pub_date, tags=terms['post_tag'],
                                     categories=terms['category'],
                                     author=users[entry.author],
                                     featured_image=featured_image)

                # Get the comments from the xml doc.
                for c in xmlitem.getElementsByTagName('wp:comment'):
                    name = self.get_text(c, 'wp:comment_author')
                    email = self.get_text(c, 'wp:comment_author_email')
                    url = self.get_text(c, 'wp:comment_author_url')
                    body = self.get_text(c, 'wp:comment_content')
                    pub_date = self.get_text(c, 'wp:comment_date_gmt')
                    fmt = '%Y-%m-%d %H:%M:%S'
                    pub_date = datetime.strptime(pub_date, fmt)
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                    self.add_comment(post=post, name=name, email=email,
                                     body=body, website=url,
                                     pub_date=pub_date)

    def get_text(self, xml, name):
        """
        Gets the element's text value from the XML object provided.
        """
        nodes = xml.getElementsByTagName(name)[0].childNodes
        accepted_types = [Node.CDATA_SECTION_NODE, Node.TEXT_NODE]
        return ''.join([n.data for n in nodes if n.nodeType in accepted_types])

    def wp_caption(self, post):
        """
        Filters a Wordpress Post for Image Captions and renders to
        match HTML.
        """
        for match in re.finditer(r'\[caption (.*?)\](.*?)\[/caption\]', post):
            meta = '<div '
            caption = ''
            for imatch in re.finditer(r'(\w+)="(.*?)"', match.group(1)):
                if imatch.group(1) == 'id':
                    meta += 'id="%s" ' % imatch.group(2)
                if imatch.group(1) == 'align':
                    meta += 'class="wp-caption %s" ' % imatch.group(2)
                if imatch.group(1) == 'width':
                    width = int(imatch.group(2)) + 10
                    meta += 'style="width: %spx;" ' % width
                if imatch.group(1) == 'caption':
                    caption = imatch.group(2)
            parts = (match.group(2), caption)
            meta += '>%s<p class="wp-caption-text">%s</p></div>' % parts
            post = post.replace(match.group(0), meta)
        return post

    def correct_url(self, url, return_rel=False):
        """
        A utility function to test and convert wordpress image src.

        :param url:
            URL to test and convert.
        :param return_rel:
            Boolean containing wheather converted url is relative to
            `settings.MEDIA_URL`
        :return:
            Converted url if original url is wordpress one,
            original url otherwise
        """
        url_pattern = re.compile(r'https?:\/\/mozscienceblog\.wpengine\.com'
                                 r'\/wp-content\/uploads\/(?P<rel_path>.+)')

        upload = settings.MEDIA_URL
        return_string = url
        with open('import_log.txt', 'a') as e:
            m = re.match(url_pattern, url)
            if m:
                r_path = m.group('rel_path')
                if return_rel:
                    return_string = r_path
                else:
                    return_string = (upload + r_path)
            else:
                e.write(url + '\n')
        return return_string
