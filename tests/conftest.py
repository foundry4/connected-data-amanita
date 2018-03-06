"""Test fixtures for autodiscovery in Pytest"""
import pytest

from app import api as api


@pytest.fixture
def flask_app():
    api.app.testing = True
    return api.app.test_client()
