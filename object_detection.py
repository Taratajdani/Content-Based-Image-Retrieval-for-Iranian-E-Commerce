import cv2
import numpy as np
import tensorflow as tf


model = tf.keras.applications.MobileNetV2(weights='imagenet')


def detect_objects(image):

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    return "electronics"  

def extract_features(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224)) 
    image = np.expand_dims(image, axis=0) 
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    
    features = model.predict(image)
    return features.flatten()

def calculate_similarity(image1_features, image2_features):
    return np.dot(image1_features, image2_features) / (np.linalg.norm(image1_features) * np.linalg.norm(image2_features))
