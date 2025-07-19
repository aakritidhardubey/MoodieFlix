from pymongo import MongoClient
import streamlit as st

def get_user_collection():
    client=MongoClient(st.secrets["MONGO_URI"])
    db=client["moodieflix"]

    return db["users"]