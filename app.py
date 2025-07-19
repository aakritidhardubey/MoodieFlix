import streamlit as st
import requests
import base64
import os
import re
from utils.auth import check_credentials, register_user
from utils.wishlist import add_to_wishlist,get_wishlist, remove_from_wishlist

st.set_page_config(page_title="MoodieFlix 🍿", page_icon="🎥", layout="wide")

# ------------------ Session Setup -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# ------------------ CSS Utility Functions -------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_css_with_background():
    possible_images = ["image2.jpg", "image2.png", "background.jpg", "background.png"]
    img_base64 = None
    for img_path in possible_images:
        if os.path.exists(img_path):
            img_base64 = get_base64_image(img_path)
            break

    background_style = (
        f'url("data:image/jpeg;base64,{img_base64}")'
        if img_base64
        else "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    )
    st.markdown(f"""
        <style>
        .stApp {{
            background: {background_style};
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            min-height: 100vh;
        }}
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            padding: 2rem !important;
            border-radius: 16px !important;
            max-width: 100% !important;
            margin-top: 0 !important;
        }}
        .main h1 {{
            color: white !important;
            font-size: clamp(2rem, 5vw, 3rem) !important;
            font-weight: 800 !important;
            text-align: center !important;
            margin: 0 auto 2rem auto !important;
            padding: 1rem !important;
            line-height: 1.2 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            width: 100% !important;
            overflow: visible !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }}
        .main, .main p, .main div, .main span {{
            color: white !important;
        }}
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 8px !important;
            border: 1px solid #ff1493 !important;
            padding: 0.75rem !important;
        }}
        .stTextInput > div > div > input::placeholder {{
            color: rgba(255, 255, 255, 0.7) !important;
        }}
        .stButton > button {{
            background-color: #f04aa4 !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.25rem !important;
            transition: background-color 0.3s ease !important;
        }}
        .stButton > button:hover {{
            background-color: #ff69b4 !important;
        }}
        .stSpinner > div {{
            color: white !important;
        }}
        header[data-testid="stHeader"] {{
            display: flex !important;
        }}
        footer {{
            display: none !important;
        }}
        .main .element-container div[data-testid="stMarkdownContainer"] {{
            color: white !important;
        }}
        .main .element-container div[data-testid="stMarkdownContainer"] p {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        }}
        .movie-card {{
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.7) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .movie-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }}
        .movie-title {{
            color: #ff1493 !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        }}
        .movie-description {{
            color: white !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
            margin-bottom: 0.5rem !important;
        }}
        .section-title {{
            color: white !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            text-align: center !important;
            margin: 2rem 0 1rem 0 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        </style>
        """, unsafe_allow_html=True)

def css_auth():
    image_path = "image1.jpg"
    img_base64 = get_base64_image(image_path) if os.path.exists(image_path) else None
    background_style = (
        f'url("data:image/jpeg;base64,{img_base64}")'
        if img_base64
        else "linear-gradient(to right, #141E30, #243B55)"
    )

    st.markdown(f"""
    <style>
        .stApp {{
            background: {background_style};
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            min-height: 100vh;
        }}

        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.5);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
        }}

        h1 {{
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 900;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }}

        input[type="text"], input[type="password"] {{
            background-color: rgba(255, 255, 255, 0.15);
            color: white;
            border: 1px solid #ed15a2;
            border-radius: 8px;
            padding: 0.75rem;
        }}

        .stButton > button {{
            background-color: #ed15a2;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.75rem 1.25rem;
            transition: background-color 0.3s ease;
            border: none;
        }}

        .stButton > button:hover {{
            background-color: #f21b9c;
        }}

        a {{
            color: #00ced1 !important;
            font-weight: bold;
        }}

        header[data-testid="stHeader"], footer {{
            display: flex;
        }}
    </style>
    """, unsafe_allow_html=True)

# ------------------ Auth Functions -------------------
def login():
    css_auth()
    st.title("🎬 MovieFlix Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if check_credentials(username, password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid username or password.")

    if st.button("Don't have an account? Register here"):
        st.session_state.page = "register"
        st.rerun()

def register():
    css_auth()
    st.title("📽️ Register to MovieFlix")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            register_user(username, password)
            st.success("Registration successful. Please login.")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Already have an account? Login here"):
        st.session_state.page = "login"
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "login"
    st.rerun()
# ------------------ wishlist -------------------
def wishlist():
    css_auth()
    st.title("💖 Your Movie Wishlist")

    wishlist = get_wishlist(st.session_state.username)

    if not wishlist:
        st.info("No movies in your wishlist yet.")
    else:
        for movie in wishlist:
            with st.container():
                
                st.markdown(
                        f"""
                        <div style="backdrop-filter: blur(10px);border: 1px solid rgba(255, 255, 255, 0.3);border-radius: 16px;padding: 1.5rem;
                            margin: 1rem 0;box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);transition: transform 0.3s ease, box-shadow 0.3s ease;">
                            <h4 style="margin-bottom: 8px; color: #ff1493;">🎬 {movie['title']}</h4>
                            <p style="margin: 0; color:white;">{movie['description']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            cols = st.columns([0.8, 0.2])
            with cols[1]:
                if st.button("🗑 Remove", key=movie["title"]):
                    remove_from_wishlist(st.session_state.username, movie["title"])
                    st.rerun()
    
    if st.button("🔙 Back to Home"):
                st.session_state.page = "main"
                st.rerun()


# ------------------ Main App -------------------
def main_app():
    load_css_with_background()
    st.title("MoodieFlix 🍿")
    st.markdown(
        f"<h3 style='color: white;'>👋 Hello, {st.session_state.username}!</h3>",
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("## Menu")
        if st.button("💖 View Wishlist"):
            st.session_state.page = "wishlist"
            st.rerun()
        if st.button("🚪 Logout"):
            logout()

    def parse_movies(text):
        movies = []
        parts = re.split(r'\*\*([^*]+)\*\*', text)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                title = parts[i].strip()
                description = parts[i + 1].strip().split('\n')[0].strip()
                description = re.sub(r'^\s*[-–—]\s*', '', description)
                if title and description:
                    movies.append({'title': title, 'description': description})
        return movies

    def create_search_links(title):
        import urllib.parse
        encoded_title = urllib.parse.quote(re.sub(r'\s*\(\d{4}\)', '', title.strip()))
        return {
            "imdb_search": f"https://www.google.com/search?q={encoded_title}+movie+site:imdb.com",
            "youtube_trailer": f"https://www.youtube.com/results?search_query={encoded_title}+trailer",
            "rotten_tomatoes": f"https://www.google.com/search?q={encoded_title}+movie+site:rottentomatoes.com"
        }

    def display_cards(movies):
        if not movies:
            st.warning("No movies found.")
            return
        st.markdown('<h3 class="section-title">🎬 Your Movie Recommendations</h3>', unsafe_allow_html=True)
        cols = st.columns(min(len(movies), 2))
        for i, movie in enumerate(movies):
            with cols[i % len(cols)]:
                links = create_search_links(movie["title"])
                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">🎬 {movie['title']}</div>
                    <div class="movie-description">{movie['description']}</div>
                    <div style="margin-top: 1rem;">
                        <a href="{links['imdb_search']}" target="_blank">🎞️ IMDB</a> |
                        <a href="{links['youtube_trailer']}" target="_blank">🎥 Trailer</a> |
                        <a href="{links['rotten_tomatoes']}" target="_blank">🍅 Reviews</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("❤️ Add to Wishlist", key=f"wishlist_{movie['title']}"):
                    wishlist_movie = {
                    "title": movie["title"],
                    "description": movie["description"],
                    "imdb_link": links["imdb_search"],
                    "trailer_link": links["youtube_trailer"],
                    "reviews_link": links["rotten_tomatoes"]
                    }
                    add_to_wishlist(st.session_state.username, wishlist_movie)
                    st.success(f"✅ Added '{movie['title']}' to your wishlist!")

    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

    prompt = st.text_input("What do you want to watch?", placeholder="e.g., A sci-fi thriller with time travel")

    if prompt:
        with st.spinner("Finding your perfect movie..."):
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://moodieflix.streamlit.app",
                    "X-Title": "MoodieFlix Recommender"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You're a movie expert. Recommend 6-7 movies with brief descriptions. Titles in **bold**."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            recommendation = response.json()["choices"][0]["message"]["content"]
            movies = parse_movies(recommendation)
            display_cards(movies)

# ------------------ Main App Entry -------------------
def main():
    if not st.session_state.logged_in:
        if st.session_state.page == "register":
            register()
        else:
            login()
    else:
        if st.session_state.page=="wishlist":
            wishlist()
        else:
            main_app()

if __name__ == "__main__":
    main()
