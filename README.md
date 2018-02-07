# Google Container Engine Skeleton Service

Skeleton Google Container Engine (GKE) service. Implemented with the Python 2
[Flask](http://flask.pocoo.org/) microframework and running with
[Green Unicorn](http://gunicorn.org/) Python WSGI HTTP Server.

## Run Locally
1. Create a virtualenv, install dependencies:
```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
2. Run the service:
```
python3 app/hello.py
```

3. Visit the application at http://localhost:5000.

## Tests
Run tests using:
```
pytest
```

## Building & Deployment

This app is provided as with a Dockerfile which is used to build a container.
This should then be pushed to a container registry and deployed either as a
manual process or using something such as build triggers and a continuous
delivery platform like [Spinnaker](https://www.spinnaker.io/).
