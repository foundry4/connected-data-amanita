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
    assert data == {}

def test_get_items(client):
    r = client.get('/items')
    data = json.loads(r.get_data(as_text=True))
    assert data == {}

def test_get_item(client):
    r = client.get('/items/item_to_get')
    data = json.loads(r.get_data(as_text=True))
    assert data == {'item_to_get':{}}

def test_del_item(client):
    r = client.delete('/items/item_to_del')
    data = json.loads(r.get_data(as_text=True))
    assert data == {'deleted': 'item_to_del'}

def test_add_item(client):
    r = client.post('/items', data={}, content_type='application/json')
    data = json.loads(r.get_data(as_text=True))
    assert data == {'added':{}}

def test_patch_item(client):
    r = client.patch('/items/item_to_patch')
    data = json.loads(r.get_data(as_text=True))
    assert data == {'patched':'item_to_patch'}
