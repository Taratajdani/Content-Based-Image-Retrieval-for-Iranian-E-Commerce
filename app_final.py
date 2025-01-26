from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid
from object_detection import detect_objects, extract_features, calculate_similarity
from mysqlDataBase import get_db_connection, store_session_data
from image_processing import preprocess_image

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())

    file_path = f"uploaded_images/{session_id}.jpg"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image = preprocess_image(file_path)

    detected_category = detect_objects(image)

    store_session_data(session_id, file_path, detected_category)
    results = perform_image_search(file_path, detected_category)


    return JSONResponse({"top_10_results": results})

def perform_image_search(uploaded_image_path, detected_category):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE category = %s"
    cursor.execute(query, (detected_category,))
    database_images = cursor.fetchall()

    top_10_results = get_top_10_similar_images(uploaded_image_path, database_images)
    
    return top_10_results
