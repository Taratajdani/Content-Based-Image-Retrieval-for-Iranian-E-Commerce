import sqlite_utils
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def calculate_similarity(query_vector, vectors):
    similarity = cosine_similarity(query_vector, np.array(vectors))
    return similarity.flatten().tolist()

def generate_text_vector(object):
  return model.encode(object)


def create_db(db_path):
    db = sqlite_utils.Database(db_path)
    db["images"].insert_all([
    {
        'id': 1,
        'image_url': 'https://dkstatics-public.digikala.com/digikala-products/4086811.jpg?x-oss-process=image/resize,m_lfit,h_800,w_800/quality,q_90',
        'object': 'mobile',
        'product_url': 'https://www.digikala.com/product/dkp-4086811'
    },
    {
        'id': 2,
        'image_url': 'https://dkstatics-public.digikala.com/digikala-products/6372869.jpg?x-oss-process=image/resize,m_lfit,h_800,w_800/quality,q_90',
        'object': 'laptop',
        'product_url': 'https://www.digikala.com/product/dkp-6372869'
     },
    {
         'id': 3,
         'image_url': 'https://dkstatics-public.digikala.com/digikala-products/5590756.jpg?x-oss-process=image/resize,m_lfit,h_800,w_800/quality,q_90',
        'object': 'tv',
        'product_url': 'https://www.digikala.com/product/dkp-5590756'
    }
    ], pk="id")
    for item in db["images"].rows:
      db["images"].update(item['id'], {'text_vector': generate_text_vector(item['object'])})
    db.vacuum()