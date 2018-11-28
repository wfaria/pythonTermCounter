This is a project made to process text inputs and store the number of times which each word appears. It works as a REST service, with routes to send new strings to be processed or access the number of times which a specific word was processed.

It uses the microframework Flask for REST request routing and processing definition, Gunicorn as the main Web Server Gateway Interface to provide the Flask application inside of multiple workers and Gevent to monkey patch python native methods, improving the performance of networking methods by managing coroutines and other asynchronous functionalities.

The project can be installed as a Docker container, ready to be executed by the *Compose* or *Swarm* command.

## Setup

To start copy the project to your machine:

```
git clone https://github.com/wfaria/pythonTermCounter.git
```

This machine should have DockerCE and Docker-Compose installed, check this [link to know more details](https://docs.docker.com/get-started/#prepare-your-docker-environment).

You just need to call the Docker to start the service. The following commands will clean the last container built, create a new one and start it.

```
cd project_folder
docker-compose down
docker-compose build
docker-compose up
```

Try to access the localhost service to see if the server is OK. You should be able to see a simple text page like this one:

> ### Hello WorldTest!
> 
> **Hostname:** 7d3bbf4664df  
> **Visits:** 1

## Service routes

### String ingestion

There is a method on the project able to process a string input, breaking it into multiple words and normalizing them (removing diacritics, extra spaces). After that, it groups each token and return the number of times which each word appeared. This method is used by all routes from this section.

The project has two routes for word insertion. The first one process all files placed on the "initialLoadFiles" folder and insert the result into the database. The returned JSON object displays the time spent in seconds and how many words were affected by it:

```
/termCounterServer$ curl -i http://192.168.99.100/load_default
HTTP/1.1 200 OK
Server: gunicorn/19.9.0
Date: Mon, 05 Nov 2018 22:36:17 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 56

{"processTime":3.7828340000000003,"updatedTerms":31878}
```

The second method is provided as a POST request which reads the string from the request's body (using UTF-8 format). It uses the same logic from the last command:

```
/termCounterServer$ curl -i -H "Content-Type: text/plain; charset=utf-8" -X POST -d 'abalancar pudim abalançar' http://192.168.99.100/upload_terms
HTTP/1.1 201 CREATED
Server: gunicorn/19.9.0
Date: Mon, 05 Nov 2018 22:42:17 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 55

{"processTime":0.0005889999999997286,"updatedTerms":2}
```

You can use the same command to process a file from a remote machine:

```
/termCounterServer$ curl -i -H "Content-Type: text/plain; charset=utf-8" -X POST --data-binary @words_1.csv http://192.168.99.100/upload_terms
HTTP/1.1 100 Continue
HTTP/1.1 201 CREATED
Server: gunicorn/19.9.0
Date: Mon, 05 Nov 2018 22:44:33 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 46

{"processTime":3.174156,"updatedTerms":31877}
 ```
 
### Word counting

You can use the following GET request to discover how many times each word was counted by the server. The command will remove any diacritics to simplify the word grouping:

```
/termCounterServer$ curl -i http://192.168.99.100/abalançar
HTTP/1.1 200 OK
Server: gunicorn/19.9.0
Date: Mon, 05 Nov 2018 22:38:48 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 51

{"count":6,"processTime":0.00016199999999999548}
```
