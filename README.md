# FormosaMatch

## Description

Final project for Advanced Databases Master's Course - NTHU 2016



## Disclaimer
This Docker setup was done using the following links for inspiration

https://github.com/DBProductions/neo4j-flask
https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/

## Instructions - WOW!

We can use Docker for our developing infrastructure

If messing around with too many containers, try out

https://github.com/ZZROTDesign/docker-clean

	docker-clean stop
	docker-clean images

These commands will clean up your docker :)

To build our Flask+Neo4j environment, run:

	docker-compose build

And then:

	docker-compose up

The website will be available on localhost and the Neo4j panel on localhost:7474.

To enter the web container for any reason, check the name of your containers running:

	docker ps -a

And then:

	docker exec -it NAME_OF_YOUR_WEB_CONTAINER /bin/bash

For example:

	docker exec -it formosamatch_web_run_1 /bin/bash

## Starting the db

To start the DB follow the following procedures:

First, we need to create a Database with the name "formosamatch" in our PostgreSQL container

To enter the container (example, please check the name of your PostgreSQL container):

	docker exec -it formosamatch_postgres_1 /bin/bash

Inside the PostgreSQL container, access the PostgreSQL shell:

	psql -h localhost -p 5432 -U postgres --password

To create the database:

	CREATE DATABASE formosamatch;

Afterwards, outside the PostgreSQL container, we can use the commands in create_db.py to start the database:

	docker-compose run web /usr/local/bin/python create_db.py create_db
	docker-compose run web /usr/local/bin/python create_db.py db init
	docker-compose run web /usr/local/bin/python create_db.py db migrate

We can add an "admin" user just to try the databse by running:

	docker-compose run web /usr/local/bin/python create_db.py create_admin

To check if the user was added, enter the PostgreSQL container, run the PostgreSQL shell, use the formosamatch DB:

	\c formosamatch;

And then run a query on the users:

	SELECT * FROM users;

We should see the admin user that was created by create_db.py

Additionally, we can test the creation of other user by running on our terminal (need to have curl installed):

	curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"email": "test@test.com", "password": "test"}' http://localhost/api/register

This should return a JSON response like:

```json
  {
    "result": "success"
  }
```

# Info on neo4j configuration:
Because we are running on docker on dev, when creating the graph connection on app.py, we are using the docker hostname for the neo4j container, which is "neo4j". When deploying to production, please put the correct hostname or IP.

	graph = Graph('http://NEO4j_USER:NEO4j_PASS@neo4j:7474/db/data/')

To check if the Flask container can connect to the neo4j container, you can run from inside the Flask container:

	curl http://neo4j:7474

	This should return a JSON response like:

	```json
		{
			"management" : "http://neo4j:7474/db/manage/",
			"data" : "http://neo4j:7474/db/data/",
			"bolt" : "bolt://neo4j:7687"
		}
	```

Note: remember to replace with the proper neo4j hostname or IP.
