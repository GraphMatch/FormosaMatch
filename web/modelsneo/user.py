#!/usr/bin/env python
""" user model """

import uuid
from datetime import datetime
#from passlib.hash import bcrypt
from py2neo import Node, Relationship, Graph
import py2neo

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

    def __init__(self, graph, username, latitude, longitude, gender = 'woman', age = None,orientation = None,
                 sexPreference = None, locationFormatted = 'taipei', height = 0, bodyType = None, drinking = None,
                 educationValue = None, smoking = None,  minAge = None, maxAge = None
                 ):
        """ set values """
        self.graph = graph
        self.username = username
        self.latitude = latitude
        self.longitude = longitude
        self.gender = gender
        self.age = age
        self.orientation = orientation
        self.sexPreference = sexPreference
        self.locationFormatted = locationFormatted
        self.height = height
        self.bodyType = bodyType
        self.drinking = drinking
        self.educationValue = educationValue
        self.smoking = smoking
        self.minAge = minAge
        self.maxAge = maxAge
        self.version = py2neo.__version__.split('.')


    def find(self):
        #""" find a user by email or username """
        if self.username is not None:
            return self.graph.find_one("User", "username", self.username)

    def register(self):
        """ register a new user if not exists """
        user = self.find()
        if not user:
            user = Node("User",
                        username=self.username,
                        latitude=self.latitude,
                        longitude=self.longitude,
                        gender=self.gender,
                        age=self.age,
                        orientation=self.orientation,
                        sexPreference=self.sexPreference,
                        locationFormatted=self.locationFormatted,
                        height=self.height,
                        bodyType=self.bodyType,
                        drinking=self.drinking,
                        educationValue=self.educationValue,
                        smoking=self.smoking,
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
            user['height'] = self.height
            user['bodyType'] = self.bodyType
            user['drinking'] = self.drinking
            user['educationValue'] = self.educationValue
            user['smoking'] = self.smoking
            user['minAge'] = self.minAge
            user['maxAge'] = self.maxAge
            user.push()
        return True


    def get_matches(self, distance = 25, gender = None, orientation = None, sexPreference = None,
                    locationFormatted = None, minHeight = None, maxHeight = None, bodyType = None,
                    drinking = None, educationValue = None, smoking = None, minAge = None, maxAge = None,
                    startFrom = 0, resultAmount = 10):
        """Find users close to me given the preferences."""
        #setting default values
        user = self.find()
        if gender is None:
            if user['gender'] == 'woman' and user['orientation'] == 'straight':
                gender = 'man'
            elif user['gender'] == 'woman' and user['orientation'] == 'gay':
                gender = 'woman'
            elif user['gender'] == 'man' and user['orientation'] == 'straight':
                gender = 'woman'
            elif user['gender'] == 'man' and user['orientation'] == 'gay':
                gender = 'man'


        if minAge is None:
            minAge = user['age'] - 5
            if minAge < 18:
                minAge = 18

        if maxAge is None:
            maxAge = user['age'] + 5

        if sexPreference is None:
            sexPreference = user['gender']



        query = "match (a:User {username: '" + self.username + "'}),(b:User {}) "
        query = query + ' WHERE 1 = 1'
        order = ''

        #distance, expected Integer
        if distance is not None:
            query = query + ' AND toInt(distance(point(a),point(b)) / ' + str(distance) + ') <=  ' + str(distance)

        #expected 'woman' or 'man'
        if gender is not None:
            query = query + " AND (b.gender = '" + gender + "') "
            order = order + 'b.gender asc,'

        #orientation, expected 'straight', 'bisexual' or 'gay'
        if orientation is not None:
            query = query + " AND (b.orientation = '" + orientation + "' or b.orientation is null)"
            order = order + 'b.orientation asc,'

        # sexPreference, expected 'woman', 'man' or 'everyone'
        if sexPreference is not None:
            query = query + " AND (b.sexPreference = '" + sexPreference + "' or b.sexPreference is null or b.sexPreference = 'everyone')"
            order = order + 'b.sexPreference asc,'

        # locationFormatted, expected a string
        if locationFormatted is not None:
            query = query + " AND (b.locationFormatted = '" + locationFormatted + "')"
            order = order + 'b.locationFormatted asc,'

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

        # drinking, expected a string
        if drinking is not None:
            query = query + " AND (b.drinking = '" + drinking + "' or b.drinking is null)"
            order = order + 'b.drinking asc,'

       # educationValue, expected a string
        if educationValue is not None:
            query = query + " AND (b.educationModifier = 'working_on' or b.educationModifier is null)"
            query = query + " AND (b.educationValue  = '" + educationValue + "' or b.educationValue is null)"
            order = order + 'b.educationValue asc,'

        # smoking, expected a string
        if smoking is not None:
            query = query + " AND (b.smoking = '" + smoking + "' or b.smoking is null)"
            order = order + 'b.smoking asc,'

        # minAge, expected a integer for age
        if minAge is not None:
            query = query + " AND (toFloat(b.age) >= " + str(minAge) + " or b.age is null or toFloat(b.age) = 0)"
            order = order + 'b.age asc,'


        # maxHeight, expected a integer for cm
        if maxAge is not None:
            query = query + " AND (toFloat(b.age) <= " + str(maxAge) + " or b.age is null or toFloat(b.age) = 0)"

        query = query + ' RETURN b '
        if len(order)>0:
            order = order[:-1]
            query = query + 'order by ' + order

        query = query + ' skip ' + str(startFrom) + ' limit ' + str(resultAmount);
        #print(query)
        version = py2neo.__version__.split('.')
        if int(version[0]) >= 3:
            return self.graph.run(query).data()
        else:
            return self.graph.cypher.execute(query)


    def like_user(self,username):
        query = "MATCH (n:User {username: '" +self.username+ "' }) MATCH (m:User {username: '" + username + "'}) CREATE (n)-[r:LIKES]->(m)"
        if int(self.version[0]) >= 3:
            self.graph.run(query).data()
        else:
            self.graph.cypher.execute(query)
        return self


    def check_if_match(self, username):
        #check if the like is mutual
        query = "MATCH (a:User {username:'" + username + "'}), (b:User {username:'" + self.username + "'}) WHERE (a)-[:LIKES]->(b) and (b)-[:LIKES]->(a) return a"
        if int(self.version[0]) >= 3:
            result = self.graph.run(query).data()
        else:
            result = self.graph.cypher.execute(query)
        if result is not None and result != []:
            #we got a match!!
            query = "MATCH (n:User {username: '" + self.username + "' }) MATCH (m:User {username: '" + username + "'}) CREATE (n)-[r:MATCH{matchId: (n.username + m.username)}]->(m)"
            query2 = "MATCH (n:User {username: '" + self.username + "' }) MATCH (m:User {username: '" + username + "'}) CREATE (m)-[r:MATCH{matchId: (m.username + n.username)}]->(n)"
            if int(self.version[0]) >= 3:
                self.graph.run(query).data()
                self.graph.run(query2).data()
            else:
                self.graph.cypher.execute(query)
                self.graph.cypher.execute(query2)
            return True
        return False


def get_matches(self,startFrom = 0,resultAmount = 10):
    query = "MATCH (a:User {username:'" + self.username + "'}), (b:User) WHERE (a)-[:MATCH]-(b) return b "
    query = query + ' skip ' + str(startFrom) + ' limit ' + str(resultAmount);
    if int(self.version[0]) >= 3:
        return self.graph.run(query).data()
    else:
        return self.graph.cypher.execute(query)
