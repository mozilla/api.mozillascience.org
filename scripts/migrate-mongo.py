import argparse
import psycopg2
from pymongo import MongoClient
from datetime import datetime
import copy

TODAY = datetime.today()


def construct_insert_query(mongo_obj, table, cols):
    query_start = 'INSERT INTO ' + table + '('
    query_middle = ') VALUES('
    query_end = ');'

    for key in cols:
        if key in mongo_obj and mongo_obj[key] is not None:
            query_start += key + ', '
            query_middle += '%(' + key + ')s, '

    return query_start[:-2] + query_middle[:-2] + query_end


def pg_run_batch_insert_queries(
    pgdb, pg_table, pg_cols,
    pgify_fn,
    mongo_object_list, num_of_objects,
    exists_in_pg,
    get_mongo_common_val=None
):
    count = 0
    mongo_id_pg_common_col_map = {}

    while count < num_of_objects:

        with pgdb.cursor() as cursor:

            for i in range(count, count + 10):
                mongo_object = mongo_object_list[i]

                if exists_in_pg(mongo_object) is not True:
                    obj = pgify_fn(copy.deepcopy(mongo_object))
                    cursor.execute(
                        construct_insert_query(obj, pg_table, pg_cols),
                        obj
                    )

                if get_mongo_common_val is not None:
                    mongo_match = get_mongo_common_val(mongo_object)
                    mongo_id_pg_common_col_map[mongo_match] = \
                        str(mongo_object['_id'])

                count = count + 1
                if count == num_of_objects:
                    break

    return mongo_id_pg_common_col_map


def pg_create_relations(
    primary_collection,
    pgdb, pg_table,
    pg_primary_relation_col, pg_secondary_relation_col,
    primary_map, get_secondary_id,
    mongo_ids_in_collection,
    pgify_fn=lambda obj, rel: obj,
    pg_extra_cols=None,
):
    additional_cols = ''
    pg_cols = [
        pg_primary_relation_col,
        pg_secondary_relation_col
    ]
    if pg_extra_cols is not None:
        pg_cols += pg_extra_cols
        pg_extra_cols = ['"' + val + '"' for val in pg_extra_cols]
        additional_cols = ', ' + ', '.join(pg_extra_cols)

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "' +
        pg_primary_relation_col + '", "' + pg_secondary_relation_col + '"' +
        additional_cols + ' '
        'FROM "' + pg_table + '";'
    )
    existing_relation_rows = get_cursor.fetchall()
    get_cursor.close()
    existing_relations = {}

    for relation_row in existing_relation_rows:
        if relation_row[0] not in existing_relations:
            existing_relations[relation_row[0]] = [relation_row[1]]
        else:
            existing_relations[relation_row[0]].append(relation_row[1])

    primary_objs = primary_collection.find().sort('_id')

    for obj in primary_objs:
        mongo_id = str(obj['_id'])
        obj_pg_id = primary_map.get(mongo_id)
        relations = []

        if obj_pg_id is None:
            continue

        for mongo_rel in mongo_ids_in_collection:
            if mongo_rel not in obj:
                continue
            for rel in obj[mongo_rel]:
                related_pg_id = get_secondary_id(str(rel))
                if obj_pg_id not in existing_relations or \
                   related_pg_id not in existing_relations[obj_pg_id]:
                    pgified_obj = pgify_fn({
                        pg_primary_relation_col: obj_pg_id,
                        pg_secondary_relation_col: related_pg_id
                    }, mongo_rel)
                    if pgified_obj not in relations:
                        relations.append(pgified_obj)

        with pgdb.cursor() as cursor:
            for relation in relations:
                cursor.execute(
                    construct_insert_query(relation, pg_table, pg_cols),
                    relation
                )


def pg_create(
    collection,
    pgdb, pg_table, pg_cols,
    mongo_match_col, pg_match_col,
    pgify_fn,
    map_var_name
):
    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "' + pg_match_col +
        '" FROM "' + pg_table + '";'
    )
    existing_objects = get_cursor.fetchall()
    get_cursor.close()

    for i in range(0, len(existing_objects)):
        existing_objects[i] = existing_objects[i][0]

    mongo_objects = collection.find().sort('_id')

    def exists_in_pg_fn(mongo_object):
        return mongo_object[mongo_match_col] in existing_objects

    mongo_map = pg_run_batch_insert_queries(
        pgdb=pgdb,
        pg_table=pg_table,
        pg_cols=pg_cols,
        pgify_fn=pgify_fn,
        mongo_object_list=mongo_objects,
        num_of_objects=mongo_objects.count(),
        exists_in_pg=exists_in_pg_fn,
        get_mongo_common_val=lambda mongo_obj: mongo_obj[mongo_match_col]
    )

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "id", "' + pg_match_col +
        '" FROM "' + pg_table + '";'
    )
    pg_objects = get_cursor.fetchall()
    get_cursor.close()

    globals()[map_var_name] = {}
    for pg_object in pg_objects:
        if pg_object[1] in mongo_map:
            globals()[map_var_name][mongo_map[pg_object[1]]] = pg_object[0]


def pgify_user(mongo_user):
    global TODAY
    mongo_user['github_username'] = mongo_user.pop('github_id', None)
    mongo_user['biography'] = mongo_user.pop('bio', None)
    mongo_user['twitter_handle'] = mongo_user.pop('twitter_id', None)
    mongo_user['date_updated'] = mongo_user.pop('updatedAt', TODAY)
    mongo_user['date_created'] = mongo_user.pop('createdAt', None)
    if mongo_user['date_created'] is None:
        mongo_user['date_created'] = mongo_user['date_updated']
    mongo_user['role'] = mongo_user.pop('role', 'member')
    mongo_user['designation'] = mongo_user.pop('title', None)

    return mongo_user


def pg_create_users(collection, pgdb):
    pg_create(
        collection=collection,
        pgdb=pgdb,
        pg_cols=[
            'name', 'username', 'designation',
            'email', 'location', 'biography',
            'github_username', 'twitter_handle', 'avatar_url',
            'blog', 'company', 'date_created',
            'date_updated', 'role',
        ],
        pg_match_col='username',
        mongo_match_col='username',
        pg_table='users_user',
        pgify_fn=pgify_user,
        map_var_name='USER_MAPPING'
    )


def pgify_project(mongo_project):
    global TODAY
    mongo_project['name'] = mongo_project.pop('title', None)
    github = mongo_project.pop('github', {
        'user': '',
        'repo': ''
    })
    mongo_project['github_owner'] = github.pop('user', '')
    mongo_project['github_repository'] = github.pop('repo', '')
    mongo_project['institution'] = mongo_project.pop('institute', None)
    status = mongo_project.pop('status', None)
    if status == 'active':
        mongo_project['status'] = 'Active'
    elif status == 'complete':
        mongo_project['status'] = 'Completed'
    elif status == 'closed':
        mongo_project['status'] = 'Closed'
    else:
        mongo_project['status'] = 'Under Review'
    mongo_project[
        'scientific_benefits'
    ] = mongo_project.pop('scientific_need', None)
    mongo_project['date_updated'] = mongo_project.pop('updatedAt', TODAY)
    mongo_project['date_created'] = mongo_project.pop('createdAt', None)
    if mongo_project['date_created'] is None:
        mongo_project['date_created'] = mongo_project['date_updated']

    return mongo_project


def pg_create_projects(collection, pgdb):
    pg_create(
        collection=collection,
        pgdb=pgdb,
        pg_cols=[
            'name', 'project_url', 'slug',
            'github_owner', 'github_repository', 'image_url',
            'institution', 'description', 'short_description',
            'status', 'date_created', 'date_updated',
            'license',
        ],
        pg_match_col='name',
        mongo_match_col='title',
        pg_table='projects_project',
        pgify_fn=pgify_project,
        map_var_name='PROJECT_MAPPING'
    )


def pgify_event(mongo_event):
    global TODAY
    mongo_event['name'] = mongo_event.pop('title', None)
    mongo_event['date_updated'] = mongo_event.pop('updatedAt', TODAY)
    mongo_event['date_created'] = mongo_event.pop('createdAt', None)
    if mongo_event['date_created'] is None:
        mongo_event['date_created'] = mongo_event['date_updated']
    mongo_event['starts_at'] = mongo_event.pop('start', None)
    mongo_event['ends_at'] = mongo_event.pop('end', None)
    mongo_event['location'] = mongo_event.pop('where', None)
    mongo_event['additional_notes'] = mongo_event.pop('notes', None)

    return mongo_event


def pg_create_events(collection, pgdb):
    pg_create(
        collection=collection,
        pgdb=pgdb,
        pg_cols=[
            'name', 'image_url', 'description',
            'date_created', 'date_updated', 'starts_at',
            'ends_at', 'location', 'additional_notes',
            'slug',
        ],
        pg_match_col='name',
        mongo_match_col='title',
        pg_table='events_event',
        pgify_fn=pgify_event,
        map_var_name='EVENT_MAPPING'
    )


def pg_create_tags(collection, pgdb):
    global PROJECT_MAPPING
    projects = collection.find().sort('_id')
    tags = []

    get_cursor = pgdb.cursor()
    get_cursor.execute('SELECT "id", "name" FROM "projects_tag";')
    existing_tag_rows = get_cursor.fetchall()
    get_cursor.close()

    existing_tags = {}
    for existing_tag_row in existing_tag_rows:
        existing_tags[existing_tag_row[1]] = existing_tag_row[0]

    for project in projects:
        mongo_id = str(project['_id'])
        pg_id = PROJECT_MAPPING.get(mongo_id)
        if pg_id is not None:
            if 'languages' in project:
                for project_tag in project['languages']:
                    if project_tag not in existing_tags and \
                       project_tag not in tags:
                        tags.append(project_tag)
            if 'wanted' in project:
                for project_tag in project['wanted']:
                    if project_tag not in existing_tags and \
                       project_tag not in tags:
                        tags.append(project_tag)

    pg_run_batch_insert_queries(
        pgdb=pgdb,
        pg_table='projects_tag',
        pg_cols=['name'],
        pgify_fn=lambda tag: {'name': tag},
        mongo_object_list=tags,
        num_of_objects=len(tags),
        exists_in_pg=lambda tag: tag in existing_tags
    )

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "id", "name" FROM "projects_tag";'
    )
    pg_tags = get_cursor.fetchall()
    get_cursor.close()

    tag_map = {}
    for tag in pg_tags:
        tag_map[tag[1]] = tag[0]

    pg_create_relations(
        primary_collection=collection,
        pgdb=pgdb,
        pg_table='projects_project_tags',
        pg_primary_relation_col='project_id',
        pg_secondary_relation_col='tag_id',
        primary_map=PROJECT_MAPPING,
        get_secondary_id=lambda rel: tag_map[rel],
        mongo_ids_in_collection=['languages', 'wanted']
    )


def pg_create_categories(collection, pgdb):
    global PROJECT_MAPPING
    projects = collection.find().sort('_id')
    cats = []

    get_cursor = pgdb.cursor()
    get_cursor.execute('SELECT "id", "name" FROM "projects_category";')
    existing_cat_rows = get_cursor.fetchall()
    get_cursor.close()

    existing_cats = {}
    for existing_cat_row in existing_cat_rows:
        existing_cats[existing_cat_row[1]] = existing_cat_row[0]

    for project in projects:
        mongo_id = str(project['_id'])
        pg_id = PROJECT_MAPPING.get(mongo_id)
        if pg_id is not None:
            if 'subjects' in project:
                for project_cat in project['subjects']:
                    if project_cat not in existing_cats and \
                       project_cat not in cats:
                        cats.append(project_cat)

    pg_run_batch_insert_queries(
        pgdb=pgdb,
        pg_table='projects_category',
        pg_cols=['name'],
        pgify_fn=lambda category: {'name': category},
        mongo_object_list=cats,
        num_of_objects=len(cats),
        exists_in_pg=lambda cat: cat in existing_cats
    )

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "id", "name" FROM "projects_category";'
    )
    pg_categories = get_cursor.fetchall()
    get_cursor.close()

    category_map = {}
    for category in pg_categories:
        category_map[category[1]] = category[0]

    pg_create_relations(
        primary_collection=collection,
        pgdb=pgdb,
        pg_table='projects_project_categories',
        pg_primary_relation_col='project_id',
        pg_secondary_relation_col='category_id',
        primary_map=PROJECT_MAPPING,
        get_secondary_id=lambda rel: category_map[rel],
        mongo_ids_in_collection=['subjects']
    )


def pg_create_resource_links(collection, pgdb):
    global PROJECT_MAPPING
    projects = collection.find().sort('_id')
    links = []

    get_cursor = pgdb.cursor()
    get_cursor.execute('SELECT "id", "url" FROM "projects_resourcelink";')
    existing_link_rows = get_cursor.fetchall()
    get_cursor.close()

    existing_links = {}
    for existing_link_row in existing_link_rows:
        existing_links[existing_link_row[1]] = existing_link_row[0]

    for project in projects:
        mongo_id = str(project['_id'])
        pg_id = PROJECT_MAPPING.get(mongo_id)
        if pg_id is not None:
            if 'links' in project:
                for project_link in project['links']:
                    if project_link['link'] not in existing_links and \
                       project_link not in links:
                        project_link['project_id'] = pg_id
                        links.append(project_link)

    def pgify_fn(mongo_object):
        mongo_object['url'] = mongo_object['link']
        return mongo_object

    pg_run_batch_insert_queries(
        pgdb=pgdb,
        pg_table='projects_resourcelink',
        pg_cols=['url', 'title', 'project_id'],
        pgify_fn=pgify_fn,
        mongo_object_list=links,
        num_of_objects=len(links),
        exists_in_pg=lambda link: link['link'] in existing_links
    )


def pg_create_user_project_relation(project_collection, pgdb):
    global PROJECT_MAPPING, USER_MAPPING

    def pgify_fn(obj, mongo_rel_name):
        if mongo_rel_name is 'lead':
            obj['role'] = 'Lead'
        else:
            obj['role'] = 'Volunteer'
        return obj

    pg_create_relations(
        primary_collection=project_collection,
        pgdb=pgdb,
        pg_table='users_userproject',
        pg_primary_relation_col='project_id',
        pg_secondary_relation_col='user_id',
        primary_map=PROJECT_MAPPING,
        get_secondary_id=lambda rel: USER_MAPPING[rel],
        mongo_ids_in_collection=['lead', 'contributors'],
        pgify_fn=pgify_fn,
        pg_extra_cols=['role']
    )


def pg_create_project_event_relation(project_collection, pgdb):
    global PROJECT_MAPPING, EVENT_MAPPING

    pg_create_relations(
        primary_collection=project_collection,
        pgdb=pgdb,
        pg_table='events_event_projects',
        pg_primary_relation_col='project_id',
        pg_secondary_relation_col='event_id',
        primary_map=PROJECT_MAPPING,
        get_secondary_id=lambda rel: EVENT_MAPPING[rel],
        mongo_ids_in_collection=['events']
    )


def pg_create_user_event_relation(event_collection, pgdb):
    global USER_MAPPING, EVENT_MAPPING

    pg_create_relations(
        primary_collection=event_collection,
        pgdb=pgdb,
        pg_table='events_event_attendees',
        pg_primary_relation_col='event_id',
        pg_secondary_relation_col='user_id',
        primary_map=EVENT_MAPPING,
        get_secondary_id=lambda rel: USER_MAPPING[rel],
        mongo_ids_in_collection=['attending']
    )

    pg_create_relations(
        primary_collection=event_collection,
        pgdb=pgdb,
        pg_table='events_event_facilitators',
        pg_primary_relation_col='event_id',
        pg_secondary_relation_col='user_id',
        primary_map=EVENT_MAPPING,
        get_secondary_id=lambda rel: USER_MAPPING[rel],
        mongo_ids_in_collection=['facilitators']
    )


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Migrate existing data from the '
                'old Mozilla Science MongoDB database\n'
                'to the new Mozilla Science Postgres database. '
                'You are required to\n'
                'provide credentials for both databases '
                'by passing it through the connection uris.'
)

parser.add_argument(
    '-m', '--mongodb',
    required=True,
    metavar='<uri>',
    help='MongoDB connection uri formatted as\n'
         'mongodb://<username>:<password>@<hostname>:<port>/<database>',
)
parser.add_argument(
    '-p', '--postgres',
    required=True,
    metavar='<uri>',
    help='Postgres connection uri formatted as\n'
         'postgresql://<username>:<password>@<hostname>:<port>/<database>',
)

args = parser.parse_args()

mongodb = MongoClient(args.mongodb)
mongodb_dbname = args.mongodb.split('/')[-1]

with psycopg2.connect(args.postgres) as pgdb:
    pg_create_users(mongodb[mongodb_dbname].users, pgdb)
    pg_create_projects(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_events(mongodb[mongodb_dbname].events, pgdb)
    pg_create_tags(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_categories(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_resource_links(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_user_project_relation(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_project_event_relation(mongodb[mongodb_dbname].projects, pgdb)
    pg_create_user_event_relation(mongodb[mongodb_dbname].events, pgdb)

mongodb.close()
pgdb.close()
