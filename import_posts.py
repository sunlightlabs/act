#!/usr/bin/env python
from MySQLdb.cursors import DictCursor
from pymongo.binary import Binary
from pymongo.connection import Connection
from saucebrush.emitters import DebugEmitter, MongoDBEmitter
from saucebrush.filters import Filter, FieldModifier
import MySQLdb
import re
import saucebrush

class MySQLSource(object):
    def __init__(self, conn, query):
        self.conn = conn
        self.query = query
    def __iter__(self):
        c = self.conn.cursor()
        c.execute(self.query)
        row = c.fetchone()
        while row:
            yield row
            row = c.fetchone()
        c.close()

class MetaFilter(Filter):
    def __init__(self, conn, *args, **kwargs):
        super(MetaFilter, self).__init__(*args, **kwargs)
        self.conn = conn
    def process_record(self, record):
        query = """
            SELECT post_id, meta_key, meta_value
            FROM oh_postmeta
            WHERE post_id = %s
            LIMIT 2
        """
        record['meta'] = {}
        c = self.conn.cursor()
        c.execute(query, (record['ID'],))
        for row in c.fetchall():
            record['meta'][row['meta_key']] = row['meta_value']
        c.close()
        return record

class TagFilter(Filter):
    def __init__(self, conn, *args, **kwargs):
        super(TagFilter, self).__init__(*args, **kwargs)
        self.conn = conn
    def process_record(self, record):
        query = """
            SELECT t.name
            FROM oh_term_relationships tr
            INNER JOIN oh_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
            INNER JOIN oh_terms t ON tt.term_id = t.term_id
            WHERE tr.object_id = %s;
        """
        record['tags'] = []
        c = self.conn.cursor()
        c.execute(query, (record['ID'],))
        for row in c.fetchall():
            record['tags'].append(row['name'])
        c.close()
        record['tags'] = ", ".join(record['tags'])
        return record

class ContentFilter(Filter):
    def process_record(self, record):
        record['post_content'] = re.sub('<!--.*?-->', '', record['post_content'])
        record['post_excerpt'] = re.sub('<!--.*?-->', '', record['post_excerpt'])
        return record

conn = MySQLdb.connect(
    host='www.theopenhouseproject.com',
    user='openhouse',
    passwd='ohp',
    db='openhouse',
    cursorclass=DictCursor
)

#
# dump posts
# 

query = """
    SELECT p.ID, p.post_author, u.user_login,
        p.post_date, p.post_date_gmt, p.post_modified, p.post_modified_gmt,
        p.post_content, p.post_title, p.post_category, p.post_excerpt, p.guid, p.post_type
    FROM oh_posts p
    INNER JOIN oh_users u ON p.post_author = u.ID
    INNER JOIN oh_term_relationships tr ON p.ID = tr.object_id
    INNER JOIN oh_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
    INNER JOIN oh_terms t ON tt.term_id = t.term_id
    WHERE p.post_status = 'publish' AND p.post_type = 'post' AND (t.name = 'act' or t.name = 'The Day in Transparency')
    ORDER BY p.post_date DESC
"""

mongo = Connection()

saucebrush.run_recipe(
    MySQLSource(conn, query),
    MetaFilter(conn),
    TagFilter(conn),
    ContentFilter(),
    FieldModifier(('post_content','post_excerpt'), lambda x: Binary(x)),
    MongoDBEmitter('openhouse', 'blog', drop_collection=True, conn=mongo),
    #DebugEmitter(),
)

for d in mongo['openhouse']['blog'].find():
    print "------", d['post_title']

conn.close()
