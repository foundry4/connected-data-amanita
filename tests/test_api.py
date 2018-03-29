def test_api_root_status(flask_app):
    """Requests to the root should return 200"""
    r = flask_app.get('/')
    assert r.status_code == 200


def test_fake_endpoint(flask_app):
    """Requests to an invalid endpoint should 404"""
    r = flask_app.get('/fake_endpoint')
    assert r.status_code == 404
