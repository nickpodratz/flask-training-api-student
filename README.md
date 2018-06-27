# Flask Training REST API
This project contains a simple [Flask](http://flask.pocoo.org/) application.
Flask is a Python based microframework to build small to mid sized applications and APIs.

We wrote an OpenAPI v3 definition that defines the endpoint that should be implemented in this exercise.
You can find the definition file in this repository at [docs/api-definition.yml](docs/api-definition.yml).
We recommend to view the definition [here](https://www-technologien.pages.rechenknecht.net/flask-training-api-reference/api).

## Quickstart
We put a very basic implementation at [app/views_v1.py](app/views_v1.py). 
Please clone this repository on your machine and complete the tasks given in the comments.
Please have a look at [docs/api-definition.yml](docs/api-definition.yml) for a definition of the endpoints that should be implemented.

## Tasks
In this assignment we will build a REST API which serves pictures with metadata from a DB.
These pictures we feed into the DB by ourself by allowing clients to call `v1/images/fetch` method.

To have some data to play with, we are using a freely available image set normally used for Deep Learning you can find [here](https://image-annotations.marschke.me/NAACL/).

You are supposed to perform the following tasks:

1. Read this README and make sure you understand it
1. Look into the code, understand what it is doing in general
1. Answer questions stated in `get_answers` in [app/views_v1.py](app/views_v1.py)
1. Implement the API itself by looking at https://www-technologien.pages.rechenknecht.net/flask-training-api-reference/api or using the API definition directly: [docs/api-definition.yml](docs/api-definition.yml)
    1. Make sure you understood the concept of routes and Blueprints / API-Versioning by Paths
    1. Try to run the API and test it with a simple request (such as the curl request below)
    1. We suggest you to start with the `/images/fetch` route because it will get the data into your DB
    1. Implement other get requests, most simple one is the request for one image. To get image data from database check out the Peewee documentation.
1. Hand in your solution as stated in the route `/v1/answers` 

## Getting started
This repository contains a generic Flask REST API framework, which contains mainly the Flask library itself and some other helpful tools.
One of these tools is the Flask wrapper, which takes care of helpful error messages in case of a program failure (500 Server Error) and provides some cool additional features to deal with new web security stuff such as CORS (check it out ;) ).

**Please check out [this guide](https://blog.philipphauer.de/restful-api-design-best-practices/) for best practices in RESTful API design.**

You will also find an Object to Relational Mapping (ORM) library named [Peewee](http://docs.peewee-orm.com/en/latest/) to handle connections to our database. If you are not familiar with an ORM you should check out [this neat guide](https://stackoverflow.com/questions/1279613/what-is-an-orm-and-where-can-i-learn-more-about-it#answer-1279678).
Because we were lazy people we created a little wrapper for Peewee as well, which makes some integration into Flask a little bit easier.
Therefore to access the database object you have to import the `database_holder` from `app` to access the database object itself.
You need this for doing cool things like
```python
with database_holder.database.transaction():
    image_object = Image(someProp='someValue').save()
    
    # Here could arise an Exception in case of program failure
    # If it is breaking here, all actions done in the transaction will be reverted by the DBMS.
    # So you will not get a state, which is invalid. 
    
    Caption(someOtherProp='someValue', image=image_object)
```

We recommend you to use an IDE like PyCharm for developing this piece of software.
If you are not familiar with IDEs in general you should use this project as a starting point.
Trust us, you will have many (Python) projects where a nice IDE is a real gamechanger.

## Development setup
You have to set the correct PythonPath when executing the tests to the base directory of this project.
The PythonPath is the base path for the Python interpreter, which is used for resolving imports.
When you are executing the `run.py` file from the project root, you most likely will not have to modify your PythonPath.

In order to execute this project, you have to have a recent Python Interpreter (we recommend at least Python 3.6, 3.5 should work as well, Python 2 is not working) with pip (normally installed along).
Also you have to install all the project requirements stated in `requirements.txt`.
You can do so by executing `pip3 install -r requirements.txt` in your project folder.

Please take note that you will use `lxml` later on in the project.
`lxml` is a Python wrapper for `libxml`, which allows you to parse XML files easily.
Therefore you may have to install the `lxml` library on your system (on Linux and Mac, Windows is using a static build provided by pip).
Check out [this](https://lxml.de/installation.html) website how to install `lxml` on your system (Mac and Linux).

This project contains a lot of stub code, so you will not have to understand all code in it.
For your assignments a good starting point should be the file `app/views_v1.py`, which contains the route definitions.
Also you should check out the directory `app/models` where you can find all of the Database models we use.
Because we are no Database lecture we defined the models for you.
But probably it is important to you to understand how foreign keys work and why they exist.

In our case you can navigate through the foreign keys from one side by accessing `image` and from the other through the `backref` `captions`.

Pro tip: We recommend you to use a Python venv (check this out), but it should work "native" as well.

## Run the API
To run the API simply execute `python3 run.py` in project root.

After successful starting (you should see something like this in your terminal):

```
* Serving Flask app "app" (lazy loading)
* Environment: production
WARNING: Do not use the development server in a production environment.
Use a production WSGI server instead.
* Debug mode: off
```

you can access your API for example by the following command:

```bash
curl http://localhost:5000/v1/tasks
```

### Manual testing
You can access your API with almost every HTTP client on your PC.
For an easy way to test different operations (POST, GET, PUT, PATCH) we recommend to use [Postman](https://www.getpostman.com/) (or simply write tests ;) ),

### Executing tests
Try `python3 -m unittest discover -p 'Test*.py'` after setting up your development environment.

If you are using PyCharm you can use the built in test environment as well.
Just add a new run config `Python tests` -> `unittest` pointing to the test directory of this project.
As a pattern please provide `Test*.py` because we do not use the standard pattern for our tests.

## Writing tests
We do not require you but encourage you to write tests for your application. You can do so by adding methods beginning with `test_` in `tests/TestBlueprintV1.py`.

We are using the `flask_testing` [framework](https://github.com/jarus/flask-testing) to execute our tests - just in case you want a reference.

### Linter
If you are really ambitious you can run `pylint` with our own flavour.
Because you are so ambitious you can pick up the command right from our `.gitlab-ci.yml`, which we are using normally for all our projects.

### GitLab
Just in case you want to use the automated test and linter feature you have to upload the code simply to a GitLab instance with a configured worker on it.

## Docker
The following section is just for your information. You do not have to use Docker or understand it at all (at this moment).

We provide a simple Docker file for you, which should have all features you need.
If you think it would be better to use another Docker base you can surely do it as long as you ensure that you expose your web server on port `8080`.

You can build the Docker container by executing `docker build .` (you should define `--tag=someTag` to use the image later on).

If you are new to Docker, please check out [this](https://docs.docker.com/get-started/) little guide which explains the core concepts (you only need part 1 and 2).
Also you should get information about how to build a Docker container.

Please make sure you can build the Docker container before handing in your solution.
We will grade the software in the container and because you want to get some credits for this assignment you should make sure that we can build the container right off.

## Ok, I really do not know what I am supposed to do
If you have any questions left or found a bug in our stub code, please mail us at `www-coding@lists.myhpi.de`.
We will be happy to help you.
