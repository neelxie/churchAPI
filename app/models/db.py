import psycopg2
import psycopg2.extras
from pprint import pprint
import simplejson as json
import os

class DatabaseConnection:
    def __init__(self):
        
        try:
            self.connection = psycopg2.connect(
                dbname="church",
                user='postgres',
                host='localhost',
                password='donthack',
                port=5432)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            print('Connected to the database successfully')
    
        except:
            pprint("Failed to connect to database.")

    def create_db_tables(self):
        create_table = "CREATE TABLE IF NOT EXISTS users \
            ( name VARCHAR(15) NOT NULL, \
            email VARCHAR(20) UNIQUE, \
            church VARCHAR REFERENCES churches(church_id), \
            permission VARCHAR DEFAULT 'Admin', \
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
            created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            user_id SERIAL UNIQUE PRIMARY KEY);"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS posts \
            (post_id SERIAL UNIQUE PRIMARY KEY, \
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
            created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            title VARCHAR(30) NOT NULL, \
            mediaUrl VARCHAR(200) NOT NULL, \
            approved BOOLEAN DEFAULT FALSE, \
            post_type VARCHAR DEFAULT 'text', \
            author INTEGER REFERENCES users(user_id), \
            passage VARCHAR(200) NOT NULL, \
            parent_post_id INTEGER DEFAULT 0, \
            relatedUpload INTEGER REFERENCES upload(upload_id));"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS churches \
            (church_id SERIAL UNIQUE PRIMARY KEY, \
            created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
            church_name VARCHAR(15) NOT NULL);"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS notifications \
            (notification_id SERIAL UNIQUE PRIMARY KEY, \
            note_text VARCHAR(50) NOT NULL, \
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
            seen BOOLEAN NOT NULL \
            related_post INTEGER REFERENCES posts(post_id), \
            recipient INTEGER REFERENCES users(user_id));"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS uploads \
            (upload_id SERIAL UNIQUE PRIMARY KEY, \
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
            uploader INTEGER REFERENCES users(user_id), \
            upload_url VARCHAR(200) NOT NULL );"
        self.cursor.execute(create_table)

    def add_user(self, name, email, church, permission):
        query = "INSERT INTO users (name, email, church, permission) VALUES ('{}', '{}', '{}', '{}') RETURNING *;".format(name, email, church, permisssion)
        self.cursor.execute(query)
        new_user = self.cursor.fetchone()
        return new_user


    def add_post(self, title, mediaUrl, post_type, author, passage, parent_post_id, relatedUpload):

        query = "INSERT INTO posts (title, mediaUrl, post_type, author, passage, parent_post_id, relatedUpload) VALUES ('{}', '{}', '{}', '{}', '{}', '{}','{}')RETURNING *;".format(
            title, mediaUrl, post_type, author, passage, parent_post_id, relatedUpload)
        self.cursor.execute(query)
        testimony = self.cursor.fetchone()
        return testimony

    def create_church(self, church_name):
        query = "INSERT INTO churches (church_name) VALUES ('{}') RETURNING *;".format(
            church_name)
        self.cursor.execute(query)
        church = self.cursor.fetchone()
        return church

    def add_notification(self, note_text, seen, related_post, recipient):
        query = "INSERT INTO notifications (note_text, seen, related_post, recipient) VALUES ('{}', '{}', '{}', '{}')RETURNING *;".format(
            note_text, seen, related_post, recipient)
        self.cursor.execute(query)
        notification = self.cursor.fetchone()
        return notification

    def add_upload(self, uploader, upload_url): # to be handled by cloudinary
        query = "INSERT INTO uploads (uploader, upload_url) VALUES ('{}', '{}')RETURNING *;".format(
            uploader, upload_url)
        self.cursor.execute(query)
        upload = self.cursor.fetchone()
        return upload

    def get_users(self):
        query = "SELECT * FROM users;"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        return users

    def all_churches(self, created_by):
        query = "SELECT * FROM churches;"
        self.cursor.execute(query)
        churchz = self.cursor.fetchall()
        return churchz

    def change_role(self, permission, user_id):
        query = "UPDATE users SET permission = '{}' WHERE user_id = '{}';".format(
            permission, user_id)
        self.cursor.execute(query)

    def delete_post(self, post_id, user_id):
        query = "DELETE FROM posts WHERE post_id = '{}' and user_id='{}';".format(
            post_id, user_id)
        self.cursor.execute(query)

    def drop_tables(self):
        query = "DROP TABLE churches;DROP TABLE users;DROP TABLE uploads;DROP TABLE posts;"
        self.cursor.execute(query)
        return "Tables-dropped"

if __name__ == '__main__':
    db = DatabaseConnection()
