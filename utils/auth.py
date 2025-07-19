import bcrypt
from utils.db import get_user_collection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_credentials(username, password):
    users = get_user_collection()
    user = users.find_one({"username": username})
    
    if user:
        stored_hash = user["password"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    
    return False

def register_user(username, email, password):
    users = get_user_collection()
    hashed = hash_password(password)
    users.insert_one({
        "username": username,
        "password": hashed ,
        "wishlist":[]
    })
