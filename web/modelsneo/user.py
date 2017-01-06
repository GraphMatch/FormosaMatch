#!/usr/bin/env python
""" user model """

import uuid
from datetime import datetime
#from passlib.hash import bcrypt
from py2neo import Node, Relationship, Graph

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


    def get_matches(self, distance = None, gender = None, orientation = None, sexPreference = None,
                    locationFormatted = None, status = None, language = None, ethnicity = None, minHeight = None,
                    maxHeight = None, bodyType = None, cats = None, childrenHave = None, diet = None, dogs = None,
                    drinking = None, drugs = None, educationValue = None, monogamous = None, sign = None,
                    smoking = None, religionValue = None, weed = None, minAge = None, maxAge = None, startFrom = 0,
                    resultAmount = 10):
        """Find users close to me given the preferences."""
        query = "match (a:User {username: '" + self.username + "'}),(b:User {}) "
        query = query + ' WHERE 1 = 1'
        order = ''

        #distance, expected Integer
        if distance is not None:
            query = query + ' AND toInt(distance(point(a),point(b)) / 1000) <=  ' + str(distance)

        #expected 'woman' or 'man'
        if gender is not None:
            query = query + " AND (b.gender = '" + gender + "' or b.gender is null) "
            order = order + 'b.gender asc,'

        #orientation, expected 'straight', 'bisexual' or 'gay'
        if orientation is not None:
            query = query + " AND (b.orientation = '" + orientation + "' or b.orientation is null)"
            order = order + 'b.orientation asc,'

        # sexPreference, expected 'woman', 'man' or 'everyone'
        if sexPreference is not None:
            query = query + " AND (b.sexPreference = '" + sexPreference + "' or b.sexPreference is null)"
            order = order + 'b.sexPreference asc,'

        # locationFormatted, expected a string
        if locationFormatted is not None:
            query = query + " AND (b.locationFormatted = '" + locationFormatted + "' or b.locationFormatted is null)"
            order = order + 'b.locationFormatted asc,'

        # status, expected a string
        if status is not None:
            query = query + " AND (b.status = '" + status + "' or b.status is null)"
            order = order + 'b.status asc,'

        # language, expected a string
        if language is not None:
            query = query + " AND (b.language = '" + language + "' or b.language is null)"
            order = order + 'b.language asc,'

        # ethnicity, expected a string
        if ethnicity is not None:
            query = query + " AND (b.ethnicity = '" + ethnicity + "' or b.ethnicity is null)"
            order = order + 'b.ethnicity asc,'

        # minHeight, expected a integer for cm
        if minHeight is not None:
            query = query + " AND (toFloat(b.height) >= " + str(minHeight) + " or b.height is null or toFloat(b.height) = 0)"
            order = order + 'b.heigh desc,'

        # maxHeight, expected a integer for cm
        if maxHeight is not None:
            query = query + " AND (toFloat(b.height) <= " + str(maxHeight) + " or b.height is null or toFloat(b.height) = 0)"

        # bodyType, expected a string (may become a list in future?)
        if bodyType is not None:
            query = query + " AND (b.bodyType = '" + bodyType + "' or b.bodyType is null)"
            order = order + 'b.bodyType asc,'

        # cats, expected a string
        if cats is not None:
            query = query + " AND (b.cats = '" + cats + "' or b.cats is null)"
            order = order + 'b.cats asc,'
        # children have, expected a string
        if childrenHave is not None:
            query = query + " AND (b.childrenHave = '" + childrenHave + "' or b.childrenHave is null)"
            order = order + 'b.childrenHave asc,'

        # diet, expected a string
        if diet is not None:
            query = query + " AND (b.diet = '" + diet + "' or b.diet is null)"
            order = order + 'b.diet asc,'

        # dogs, expected a string
        if dogs is not None:
            query = query + " AND (b.dogs = '" + dogs + "' or b.dogs is null)"
            order = order + 'b.dogs asc,'

        # drinking, expected a string
        if drinking is not None:
            query = query + " AND (b.drinking = '" + drinking + "' or b.drinking is null)"
            order = order + 'b.drinking asc,'

        # drugs, expected a string
        if drugs is not None:
            query = query + " AND (b.drugs = '" + drugs + "' or b.drugs is null)"
            order = order + 'b.drugs asc,'

        # educationValue, expected a string
        if educationValue is not None:
            query = query + " AND (b.educationModifier = 'working_on' or b.educationModifier is null)"
            query = query + " AND (b.educationValue  = '" + educationValue + "' or b.educationValue is null)"
            order = order + 'b.educationValue asc,'

        # drugs, expected a string
        if monogamous is not None:
            query = query + " AND (b.monogamous = '" + monogamous + "' or b.monogamous is null)"
            order = order + 'b.monogamous asc,'

        # sign, expected a string
        if sign is not None:
            query = query + " AND (b.sign = '" + sign + "' or b.sign is null)"
            order = order + 'b.sign asc,'

        # smoking, expected a string
        if smoking is not None:
            query = query + " AND (b.smoking = '" + smoking + "' or b.smoking is null)"
            order = order + 'b.smoking asc,'

        # religioValue, expected a string
        if religionValue is not None:
            query = query + " AND (b.religionModifier = 'and_its_important' or b.religionModifier is null)"
            query = query + " AND (b.religionValue  = '" + religionValue + "' or b.religionValue is null)"
            order = order + 'b.religionValue asc,'

        # weed, expected a string
        if weed is not None:
            query = query + " AND (b.weed = '" + weed + "' or b.weed is null)"
            order = order + 'b.weed asc,'

        # minAge, expected a integer for age
        if minAge is not None:
            query = query + " AND (toFloat(b.age) >= " + str(minAge) + " or b.age is null or toFloat(b.age) = 0)"
            order = order + 'b.age asc,'

        # maxHeight, expected a integer for cm
        if maxAge is not None:
            query = query + " AND (toFloat(b.age) <= " + str(maxAge) + " or b.age is null or toFloat(b.age) = 0)"

        query = query + ' RETURN b.username, b.age, b.locationFormatted, toInt(distance(point(a),point(b)) / 1000) as distance '
        query = query + 'order by ' + order + ' distance asc skip ' + str(startFrom) + ' limit ' + str(resultAmount);

        return self.graph.run(query).data()


    def like_user(self,username):
        query = "MATCH (n:User {username: '" +self.username+ "' }) MATCH (m:User {username: '" + username + "'}) CREATE (n)-[r:LIKES]->(m)"
        self.graph.run(query).data()
        return self


    def check_if_match(self, username):
        #check if the like is mutual
        query = "MATCH (a:User {username:'" + username + "'}), (b:User {username:'" + self.username + "'}) WHERE (a)-[:LIKES]->(b) and (b)-[:LIKES]->(a) return a"
        result = self.graph.run(query).data()
        print(result)
        if result is not None and result != []:
            #we go a match!!
            return True
        return False



