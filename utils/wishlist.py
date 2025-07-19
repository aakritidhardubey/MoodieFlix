from utils.db import get_user_collection

def add_to_wishlist(username, movie):
    users = get_user_collection()
    users.update_one(
        {"username": username},
        {"$addToSet": {"wishlist": movie}} 
    )

def remove_from_wishlist(username, title):
    users = get_user_collection()
    users.update_one(
        {"username": username},
        {"$pull": {"wishlist": {"title":title}}}
    )

def get_wishlist(username):
    users = get_user_collection()
    user = users.find_one({"username": username})
    return user.get("wishlist", [])
