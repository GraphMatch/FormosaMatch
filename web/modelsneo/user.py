#!/usr/bin/env python
""" user model """

import uuid
from datetime import datetime
#from passlib.hash import bcrypt
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
    def __init__(self, graph, username, latitude, longitude, email = None, gender = None, age = None,
                 orientation = None, sexPreference = None, locationFormatted = None, status = None,
                 language = None, ethnicity = None, height = None, bodyType = None, cats = None,
                 childrenHave = None, diet = None, dogs = None, drinking = None, drugs = None,
                 educationModifier = None, educationValue = None, monogamous = None, sign = None,
                 smoking = None, religionModifier = None, religionValue = None, weed = None, minAge = None, maxAge = None
                 ):
        """ set values """
        self.graph = graph
        self.email = email
        self.username = username
        self.latitude = latitude
        self.longitude = longitude
        self.gender = gender
        self.age = age
        self.orientation = orientation
        self.sexPreference = sexPreference
        self.locationFormatted = locationFormatted
        self.status = status
        self.language = language
        self.ethnicity = ethnicity
        self.height = height
        self.bodyType = bodyType
        self.cats = cats
        self.childrenHave = childrenHave
        self.diet = diet
        self.dogs = dogs
        self.drinking = drinking
        self.drugs = drugs
        self.educationModifier = educationModifier
        self.educationValue = educationValue
        self.monogamous = monogamous
        self.sign = sign
        self.smoking = smoking
        self.religionModifier = religionModifier
        self.religionValue = religionValue
        self.weed = weed
        self.minAge = minAge
        self.maxAge = maxAge


    def find(self):
        #""" find a user by email or username """
        if self.username is not None:
            return self.graph.find_one("User", "username", self.username)

    def register(self):
        """ register a new user if not exists """
        user = self.find()
        if not user:
            user = Node("User",
                        email=self.email,
                        username=self.username,
                        latitude=self.latitude,
                        longitude=self.longitude,
                        gender=self.gender,
                        age=self.age,
                        orientation=self.orientation,
                        sexPreference=self.sexPreference,
                        locationFormatted=self.locationFormatted,
                        status=self.status,
                        language=self.language,
                        ethnicity=self.ethnicity,
                        height=self.height,
                        bodyType=self.bodyType,
                        cats=self.cats,
                        childrenHave=self.childrenHave,
                        diet=self.diet,
                        dogs=self.dogs,
                        drinking=self.drinking,
                        drugs=self.drugs,
                        educationModifier=self.educationModifier,
                        educationValue=self.educationValue,
                        monogamous=self.monogamous,
                        sign=self.sign,
                        smoking=self.smoking,
                        religionModifier=self.religionModifier,
                        religionValue=self.religionValue,
                        weed=self.weed,
                        minAge=self.minAge,
                        maxAge=self.maxAge
                        )
            self.graph.create(user)
        else:
            #user = self.graph.merge_one('User', 'username', self.username)
            user['username'] = self.username
            user['latitude'] = self.latitude
            user['longitude'] = self.longitude
            user['gender'] = self.gender
            user['age'] = self.age
            user['orientation'] = self.orientation
            user['sexPreference'] = self.sexPreference
            user['locationFormatted'] = self.locationFormatted
            user['status'] = self.status
            user['language'] = self.language
            user['ethnicity'] = self.ethnicity
            user['height'] = self.height
            user['bodyType'] = self.bodyType
            user['cats'] = self.cats
            user['childrenHave'] = self.childrenHave
            user['diet'] = self.diet
            user['dogs'] = self.dogs
            user['drinking'] = self.drinking
            user['drugs'] = self.drugs
            user['educationModifier'] = self.educationModifier
            user['educationValue'] = self.educationValue
            user['monogamous'] = self.monogamous
            user['sign'] = self.sign
            user['smoking'] = self.smoking
            user['religionModifier'] = self.religionModifier
            user['religionValue'] = self.religionValue
            user['weed'] = self.weed
            user['minAge'] = self.minAge
            user['maxAge'] = self.maxAge
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
