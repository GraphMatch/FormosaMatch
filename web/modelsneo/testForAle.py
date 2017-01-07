#!/usr/bin/env python
from py2neo import Graph
from user import User as UserNeo


graph = graph = Graph('http://neo4j:neo4j1@localhost:7474/db/data/')
#graph = Graph(host='127.0.0.1', http_port=7474, user='neo4j', password='neo4j1')

#create or update user

##instance User
user = UserNeo(graph=graph, username='ale', latitude=20.312, longitude=120.4232, gender ='woman')
#create or update User
#user.register()
#get Matches
##all filters are optional
#print(user.get_browse_nodes(distance=1000, gender = 'man', orientation='straight',sexPreference='woman',
#                       minHeight=100, maxHeight=200, bodyType='fit',
#                       drinking='socially', educationValue='post_grad', smoking='no',
#                      minAge='18',maxAge='40',resultAmount=10,startFrom=10))

print(user.get_browse_nodes())

#get user Profile
#print(user.find())

#print(user.like_user('frank0728'))

#user2 = UserNeo(graph=graph, username='frank0728',latitude=2.32,longitude=43.2)
#user2.check_if_match('ale')

#print(user.get_matches())