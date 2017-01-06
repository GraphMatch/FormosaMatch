#!/usr/bin/env python
from py2neo import Graph
from user import User as UserNeo


#graph = Graph('http://neo4j:admin123@neo4j:7474/db/data/')
graph = Graph(host='127.0.0.1', http_port=7474, https_port= 7473, bolt_port=7687, user='neo4j', password='neo4j1')

#create or update user

##instance User
user = UserNeo(graph=graph, username='ale', latitude=20.312, longitude=120.4232, gender ='woman')
#create or update User
user.register()
#get Matches
##all filters are optional
print(user.get_matches(distance=1000, gender = 'man', orientation='straight',sexPreference='woman',
                       locationFormatted='taipei', status='single',language='english',ethnicity='asian',
                       minHeight=100, maxHeight=200, bodyType='fit', cats='has_cats', childrenHave = 'doesnt_have',
                       diet='omnivore',dogs='has_dogs', drinking='socially', drugs='never', educationValue='post_grad',
                       monogamous='monogamous',sign=None, smoking='no',religionValue='christianity', weed = None,
                       minAge='18',maxAge='40',resultAmount=10,startFrom=0))

print(user.get_matches())

#get user Profile
print(user.find())

print(user.like_user('frank0728').check_if_match('frank0728'))
