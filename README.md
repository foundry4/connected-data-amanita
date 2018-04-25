# Content Graph API

API for the content graph. Implemented with the Python 2
[Flask](http://flask.pocoo.org/) microframework and running with
[Green Unicorn](http://gunicorn.org/) Python WSGI HTTP Server.

## Run Locally
### 1. Create a virtualenv, install dependencies:
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

## 1. Set up location of Stardog instance
```
export STARDOG_ENDPOINT=http://$SERVER:$PORT/content-graph-test/query
export STARDOG_USER=$USERNAME
export STARDOG_PASS=$PASSWORD
```

### 2. Run the service:
```
PORT=5001 \
PYTHONPATH=.:$PYTHONPATH \
python -m app.api
```

### 3. Visit the application at http://localhost:5000.

## Style

Check if your code is PEP8 compliant:
```
pycodestyle app --max-line-length=119
```

## Tests
Run tests using:
```
py.test --cov-report term-missing --cov=app tests/ --cov-branch -vv
```

## Building & Deployment

This app is provided as with a Dockerfile which is used to build a container.
This should then be pushed to a container registry and deployed either as a
manual process or using something such as build triggers and a continuous
delivery platform like [Spinnaker](https://www.spinnaker.io/).

