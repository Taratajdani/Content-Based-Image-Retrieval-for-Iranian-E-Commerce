from fastapi import FastAPI, File, UploadFile, HTTPException
from model.object_detector import ObjectDetector
from model.image_embedder import ImageEmbedder
from utils import calculate_similarity, create_db, generate_text_vector
import io
from PIL import Image
import sqlite_utils
import os
import numpy as np

app = FastAPI()
object_detector = ObjectDetector()
image_embedder = ImageEmbedder()

DATA_PATH = os.path.join('..','..', 'data', 'database.db')
create_db(DATA_PATH)

def check_image_quality(image):
  if image.width < 200 or image.height < 200:
      return 'low'
  return 'high'


@app.post("/process_image/")
async def process_image(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image provided")
    try:
        contents = await image.read()
        image = Image.open(io.BytesIO(contents))
        quality = check_image_quality(image)
        if quality == 'low':
            return {'quality': quality}

        object_detected = object_detector.detect_objects(image)
        if object_detected is None:
            return {'quality': 'high', 'results': []}

        db = sqlite_utils.Database(DATA_PATH)
        query_vector = image_embedder.generate_embedding(image)
        similarity_scores = calculate_similarity(query_vector, [item['text_vector'] for item in db["images"].rows])
        results = []
        for i, score in enumerate(similarity_scores):
            rows = list(db["images"].rows)
            if score > 0.5:
                results.append({'image_url': rows[i]['image_url'], 'product_url': rows[i]['product_url']})
        results = sorted(results, key=lambda x: similarity_scores[rows.index(x)], reverse=True)[:10]
        return {'quality': 'high', 'results': results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))