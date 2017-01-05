#!/usr/bin/env python
""" user model """

import uuid
from datetime import datetime
from passlib.hash import bcrypt
from py2neo import Node, Relationship

def timestamp():
    """ create a timestamp """
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    """ get formated date """
    return datetime.now().strftime('%F')

class User(object):
    """ user object """
    def __init__(self, graph, email, username, latitude, longitude):
        """ set values """
        self.graph = graph
        self.email = email
        self.username = username
        self.latitude = latitude
        self.longitude = longitude

    def find(self):
        """ find a user by email or username """
        user = {}
        if self.email != None:
            user = self.graph.find_one("User", "email", self.email)
        elif self.username != None:
            user = self.graph.find_one("User", "username", self.username)

        return user

    def register(self):
        """ register a new user if not exists """
        if not self.find():
            user = Node("User",
                        email=self.email,
                        username=self.username,
                        latitude=self.latitude,
                        longitude=self.longitude,
                        )
            self.graph.create(user)

            return True
        else:
            return False

    # def get_similar_users(self):
    #     """Find three users who are most similar to the logged-in user
    #     based on tags they've both blogged about."""
    #     query = """
    #     MATCH (you:User)-[:PUBLISHED]->(:Project)<-[:TAGGED]-(tag:Tag),
    #           (they:User)-[:PUBLISHED]->(:Project)<-[:TAGGED]-(tag)
    #     WHERE you.email = {email} AND you <> they
    #     WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
    #     ORDER BY len DESC LIMIT 3
    #     RETURN they.username AS similar_user, tags
    #     """
    #
    #     return self.graph.cypher.execute(query, email=self.email)

    # def get_similar_users_lang(self):
    #     """Find three users who are most similar to the logged-in user
    #     based on languages they've both use."""
    #     query = """
    #     MATCH (you:User)-[:USE]->(l:Language)<-[:USE]-(u:User)
    #     WHERE you.email = {email} AND you <> u
    #     WITH u, COLLECT(l.name) as langs
    #     RETURN u.username AS similar_user, langs
    #     """
    #
    #     return self.graph.cypher.execute(query, email=self.email)

    # def get_commonality_of_user(self, email):
    #     """Find how many of the logged-in user's posts the other user
    #     has liked and which tags they've both blogged about. """
    #     query = """
    #     MATCH (they:User {email:{they}}),
    #           (you:User {email:{you}})
    #     OPTIONAL MATCH (they)-[:LIKED]->(project:Project)<-[:PUBLISHED]-(you)
    #     OPTIONAL MATCH (they)-[:PUBLISHED]->(:Project)<-[:TAGGED]-(tag:Tag),
    #                    (you)-[:PUBLISHED]->(:Project)<-[:TAGGED]-(tag)
    #     RETURN COUNT(DISTINCT project) AS likes, COLLECT(DISTINCT tag.name) AS tags
    #     """
    #
    #     return self.graph.cypher.execute(query, they=email, you=self.email)[0]
