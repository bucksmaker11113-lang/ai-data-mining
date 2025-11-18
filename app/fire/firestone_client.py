# app/fire/firestore_client.py

import firebase_admin
from firebase_admin import credentials, firestore

# Renderen a gcloud-key.json a projekt rootban van
def init_firestore():
    try:
        cred = credentials.Certificate("gcloud-key.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print("Firestore init error:", e)
        return None

db = init_firestore()

def save_market_data(collection, data):
    if db:
        db.collection(collection).add(data)
    return True
