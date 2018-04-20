# Content Graph API

API for reading from the Content Graph/Store. Currently, the API is capable of interfacing with two databases: 
`Stardog` (may be generalised to any `SPARQL1.1` store), and `Elasticsearch`. Client specific code resides in the 
`clients` directory and the clients are listed in `api.py`, all other code is/should be client-agnostic. 

## Run Locally
### 1. Create a virtualenv, install dependencies:
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

### 2a. Run with Stardog
```
export DB_CLIENT='stardog'
export DB_ENDPOINT=http://$SERVER:$PORT/content-graph-test/query
export DB_USER=$USERNAME
export DB_PASS=$PASSWORD
```

### 2b. Run with Elastic
```
export DB_CLIENT='elasticsearch'
export DB_ENDPOINT=http://localhost:5001
export DB_USER=$USERNAME
export DB_PASS=$PASSWORD
```
[Resources to run Elasticseaerch stack locally.](https://github.com/bbc/connected-data-elasticsearch-docker-stack)
### 3. Run the service:
```
PORT=5001 \
PYTHONPATH=.:$PYTHONPATH \
python -m app.api
```

### 4. Visit the application at http://localhost:5001.

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
NB: SPARQL client not fully covered - still need to refactor tests. 

## Building & Deployment

This app is provided as with a Dockerfile which is used to build a container.
This should then be pushed to a container registry and deployed either as a
manual process or using something such as build triggers and a continuous
delivery platform like [Spinnaker](https://www.spinnaker.io/).
