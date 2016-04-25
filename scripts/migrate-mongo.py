import argparse
import psycopg2
from pymongo import MongoClient


def construct_insert_query(mongo_obj, table, cols):
    query_start = 'INSERT INTO ' + table + '('
    query_middle = ') VALUES('
    query_end = ');'

    for key in cols:
        if key in mongo_obj and mongo_obj[key] is not None:
            query_start += key + ', '
            query_middle += '%(' + key + ')s, '

    return query_start[:-2] + query_middle[:-2] + query_end


def pg_create(collection,
              pgdb,
              pg_cols,
              pg_match_col, mongo_match_col,
              pg_table,
              pgify_fn,
              mapping_var_name):
    globals()[mapping_var_name] = {}
    mongo_mapping = {}

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "' + pg_match_col +
        '" FROM "' + pg_table + '";'
    )
    existing_objects = get_cursor.fetchall()
    get_cursor.close()

    mongo_objects = collection.find().sort('_id')
    max_count = mongo_objects.count()
    count = 0

    while count < max_count:
        with pgdb.cursor() as cursor:
            for mongo_object in mongo_objects:
                if mongo_object[mongo_match_col] not in existing_objects:
                    obj = pgify_fn(mongo_object)
                    cursor.execute(
                        construct_insert_query(obj, pg_table, pg_cols),
                        obj
                    )
                    mongo_match = mongo_object[mongo_match_col]
                    mongo_mapping[mongo_match] = mongo_object['_id']

                count = count + 1
                if count % 10 == 0 or count >= max_count:
                    break

    get_cursor = pgdb.cursor()
    get_cursor.execute(
        'SELECT "id", "' + pg_match_col +
        '" FROM "' + pg_table + '";'
    )
    pg_objects = get_cursor.fetchall()

    for pg_object in pg_objects:
        globals()[mapping_var_name][mongo_mapping[pg_object[1]]] = pg_object[0]


def pgify_user(mongo_user):
    mongo_user['github_username'] = mongo_user.pop('github_id', None)
    mongo_user['biography'] = mongo_user.pop('bio', None)
    mongo_user['twitter_handle'] = mongo_user.pop('twitter_id', None)
    mongo_user['date_updated'] = mongo_user.pop('updatedAt', None)
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
        mapping_var_name='USER_MAPPING'
    )


def pgify_project(mongo_project):
    mongo_project['name'] = mongo_project.pop('title', None)
    github = mongo_project.pop('github', {
        'user': None,
        'repo': None
    })
    mongo_project['github_owner'] = github.pop('user', None)
    mongo_project['github_repository'] = github.pop('repo', None)
    mongo_project['institution'] = mongo_project.pop('institute', None)
    status = mongo_project.pop('status', False)
    mongo_project['status'] = status in ('active', 'complete')
    mongo_project['date_updated'] = mongo_project.pop('updatedAt', None)
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
        mapping_var_name='PROJECT_MAPPING'
    )


def pgify_event(mongo_event):
    mongo_event['name'] = mongo_event.pop('title', None)
    mongo_event['date_updated'] = mongo_event.pop('updatedAt', None)
    mongo_event['date_created'] = mongo_event['date_updated']
    mongo_event['starts_at'] = mongo_event.pop('start', None)
    mongo_event['ends_at'] = mongo_event.pop('end', None)
    mongo_event['location'] = mongo_event.pop('where', None)
    mongo_event['additional_notes'] = mongo_event.pop('notes', None)


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
        mapping_var_name='EVENT_MAPPING'
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

pgdb = psycopg2.connect(args.postgres)

pg_create_users(mongodb[mongodb_dbname].users, pgdb)
pg_create_projects(mongodb[mongodb_dbname].projects, pgdb)
pg_create_events(mongodb[mongodb_dbname].events, pgdb)

mongodb.close()
