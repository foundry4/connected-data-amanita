

# TODO: HAVE GENERAL TEST FOR PARAMETERS WHERE THERE IS A DICT SHOWING WHICH PARAMETERS WHERE AND TESTED FOR EACH CLIENT
# dict also contains other forms of parameter and example values both pre processing and post processing

# TODO: SPLIT TESTS INTO API TESTS AND CLIENT-SPECIFIC TESTS

def test_api_root_status(flask_app):
    """Requests to the root should return 200"""
    r = flask_app.get('/')
    assert r.status_code == 200


def test_fake_endpoint(flask_app):
    """Requests to an invalid endpoint should 404"""
    r = flask_app.get('/fake_endpoint')
    assert r.status_code == 404
