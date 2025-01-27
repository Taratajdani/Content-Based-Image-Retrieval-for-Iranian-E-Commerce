import pytest
from fastapi import UploadFile
import io
from PIL import Image
import os
import json

@pytest.mark.asyncio
async def test_process_image_success(test_client, test_image_path):
  
    with open(test_image_path, "rb") as f:
        files = {"image": ("test_image.jpg", f, "image/jpeg")}
        response = test_client.post("/process_image/", files=files)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["quality"] == 'high'
        assert type(response_data["results"]) == list
        assert type(response_data['results']) != None

@pytest.mark.asyncio
async def test_process_image_no_image(test_client):
    response = test_client.post("/process_image/")
    assert response.status_code == 400
    assert response.json() == {'detail': 'No image provided'}

@pytest.mark.asyncio
async def test_process_image_low_quality(test_client, test_image_path):
  low_res_image = Image.new('RGB', (100, 100), color = 'red')
  image_bytes = io.BytesIO()
  low_res_image.save(image_bytes, format="JPEG")
  image_bytes = image_bytes.getvalue()
  files = {"image": ("test_image.jpg", image_bytes, "image/jpeg")}
  response = test_client.post("/process_image/", files=files)
  assert response.status_code == 200
  response_data = response.json()
  assert response_data['quality'] == 'low'
