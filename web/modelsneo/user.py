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
    def __init__(self, graph, email = None, username = None, preference = None, sex_interest = None, search_distance = None, age_interest = None, country = None, city = None, latitude = None, longitude = None):
        """ set values """
        self.graph = graph
        self.email = email
        self.username = username
        self.latitude = latitude
        self.longitude = longitude
        self.preference = preference
        self.sex_interest = sex_interest
        self.search_distance = search_distance
        self.age_interest = age_interest
        self.country = country
        self.city = city

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
        user = self.find()
        if not user:
            user = Node("User",
                        email=self.email,
                        username=self.username,
                        preference=self.preference,
                        sex_interest=self.sex_interest,
                        search_distance=self.search_distance,
                        age_interest=self.age_interest,
                        country=self.country,
                        city=self.city,
                        latitude=self.latitude,
                        longitude=self.longitude
                        )
            self.graph.create(user)
        else:
            user = self.graph.merge_one('User', 'username', self.username)
            user['email'] = self.email
            user['preference'] = self.preference
            user['sex_interest'] = self.sex_interest
            user['search_distance'] = self.search_distance
            user['age_interest'] = self.age_interest
            user['country'] = self.country
            user['city'] = self.city
            user['latitude'] = self.latitude
            user['longitude'] = self.longitude
            user.push()
        return True

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
