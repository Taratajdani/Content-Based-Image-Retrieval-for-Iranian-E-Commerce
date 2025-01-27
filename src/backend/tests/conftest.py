import pytest
from fastapi.testclient import TestClient
from api.image import app
import os
@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def test_image_path():
    return os.path.join('..', 'tests', 'test_image.jpg')