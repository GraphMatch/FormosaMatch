= Neo4j 3.0 Spatial Functions Demo
:neo4j-version: 3.0
:URL: http://www.fa-technik.adfc.de/code/opengeodb/DE.tab
//:URL: file:///Users/mh/Dropbox/Public/DE_geo.csv

== Setup

Create constraints and load raw data from CSV.

//setup
[source,cypher,subs=attributes]
----
create constraint on (c:City) assert c.name is unique;

cypher planner=rule load csv with headers from "{URL}" as row fieldterminator "\t" 
with row where row.typ = "Stadt" AND toInt(row.einwohner) > 100000 and exists(row.lat) 
with distinct {name:row.name, pop:toInt(row.einwohner),longitude:toFloat(row.lon), latitude:toFloat(row.lat)} as data
MERGE (c:City {name:data.name}) ON CREATE SET c = data
RETURN c.name, c.pop, c.longitude, c.latitude ORDER BY c.pop DESC;
----

//table


== Distance between two cities _Berlin_ and _Dresden_

[source,cypher]
----
match (a:City {name:"Berlin"}),(b:City {name:"Dresden"})
RETURN a.name, b.name, toInt(distance(point(a),point(b)) / 1000) as distance;
----

//table


== Circle

What is on the outer rim on the 250 km circle.

[source,cypher]
----
match (a:City {name:"Berlin"}),(b:City)
WITH a, b, toInt(distance(point(a),point(b)) / 1000) as distance
WHERE distance < 250
RETURN a.name, b.name, distance
ORDER BY distance DESC LIMIT 10;
----

//table

////
[source,cypher]
----
LOAD CSV WITH HEADERS FROM {URL} AS row FIELDTERMINATOR "\t" 
CREATE (:City {name:row.name, pop:toInt(row.einwohner),
        longitude:toFloat(row.lon), latitude:toFloat(row.lat)});


MATCH (a:City {name:"Berlin"}),(b:City {name:"Dresden"})
RETURN a.name, b.name, toInt(distance(point(a),point(b)) / 1000) as distance;

+---------------------------------+
| a.name   | b.name    | distance |
+---------------------------------+
| "Berlin" | "Dresden" | 165      |
+---------------------------------+

////

== Example for shortet-path with pull-in predicates

Here is no data in the dataset, just exemplary

[source,cypher]
----
MATCH (a:Loc {name:"Berlin"}),(b:Loc {name:"Dresden"})
MATCH p = shortestPath((a)-[roads:ROAD*]->(d))
WHERE NONE(r in roads WHERE r.closed or r.speed < 30)
RETURN p;
----

== Spatial Procedures

=== Overview 

Neo4j Spatial got retrofitted with Neo4j 3.0 procedures:

NOTE: `coord` parameter can be a map with {lat,lon} or {latitude,longitude} or a node with those properties or a GeographicPoint from the point() function

* spatial.addPointLayer(name) - adds a simple point layer with property-names "longitude" for x and "latitude" for y
* spatial.addNode(layerName,node) 
* spatial.addNodes(layerName, [nodes])
* spatial.distance(layerName, coord, distanceInKm) 
* spatial.bbox(layerName, minCoord, maxCoord)

* spatial.addWKTLayer(name,wktProperty)
* spatial.addWKT(layerName, wktString)
* spatial.addWKTs(layerName, [wktStrings])
* spatial.closest(layerName, wktGeometry)

* spatial.addPointLayerNamed(name, xName, yName)
* spatial.addConfiguredLayer(name, format, propertyName)
* spatial.layer(name) - returns a layer
* spatial.updateFromWKT(layerName, wktString, nodeId)


=== Build & install neo4j-spatial procedures

[source,shell]
----
git clone http://github.com/neo4j-contrib/spatial
cd spatial
mvn clean install -DskipTests assembly:single
cp target/neo4j-spatial-0.15-neo4j-3.0.0-server-plugin.jar $NEO4J_HOME/plugins/
$NEO4J_HOME/bin/neo4j restart
----

=== Add Layer

[source,cypher]
----
CALL spatial.addPointLayer('cities');
----

=== Add all Cities to Layer

[source,cypher]
----
MATCH (c:City) 
WITH collect(c) AS cities 
CALL spatial.addNodes('cities',cities) YIELD node 
RETURN count(*)
----

// altenatively but slower
// match (c:City) with c call spatial.addNode('cities',c) yield node return count(*)

----
+--------+
|count(*)|
+--------+
|61      |
+--------+
----

=== Find within Distance

[source,cypher]
----
MATCH (c:City {name:"Berlin"}) WITH c
CALL spatial.distance('cities', c , 200) YIELD node, distance
RETURN node.name AS name, round(distance) AS dist
----

----
+------------+----+
|name        |dist|
+------------+----+
|Berlin      |0   |
|Potsdam     |27  |
|Leipzig     |150 |
|Dresden     |166 |
|Wolfsburg   |179 |
|Chemnitz    |191 |
|Braunschweig|197 |
+------------+----+
----
