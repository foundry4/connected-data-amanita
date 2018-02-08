import base64
import json
import os
import pytest


import cg as api

@pytest.fixture
def client():
    api.app.testing = True
    return api.app.test_client()

def test_index(client):
    r = client.get('/')
    assert r.status_code == 200

def test_content(client):
    r = client.get('/content')
    data = json.loads(r.get_data(as_text=True))
    assert all([data == {},r.status_code == 200])