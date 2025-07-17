import streamlit as st
import requests
import base64
import os
import re

st.set_page_config(page_title="MoodieFlix 🍿", page_icon="🎥", layout="wide")

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
    
    background_style = f'url("data:image/jpeg;base64,{img_base64}")' if img_base64 else "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    
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
        background-color: rgba(0, 0, 0, 0.4) !important;
        padding: 2rem !important;
        border-radius: 12px !important;
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
        background-color: #ff1493 !important;
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
        display: none !important;
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

def parse_movies(text):
    movies = []
    
    # Split by **Title** pattern
    parts = re.split(r'\*\*([^*]+)\*\*', text)
    
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            title = parts[i].strip()
            description = parts[i + 1].strip()
            
            # Clean up description
            description = re.sub(r'^\s*[-–—]\s*', '', description)
            description = description.split('\n')[0].strip()  # Take first line
            
            if title and description:
                movies.append({'title': title, 'description': description})
    
    return movies

def display_cards(movies):
    if not movies:
        st.markdown('<div class="movie-card"><div class="movie-description">No movies found. Please try again!</div></div>', unsafe_allow_html=True)
        return
    
    st.markdown('<h3 class="section-title">🎬 Your Movie Recommendations</h3>', unsafe_allow_html=True)
    
    cols = st.columns(min(len(movies), 2))
    
    for i, movie in enumerate(movies):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title">🎬 {movie['title']}</div>
                <div class="movie-description">{movie['description']}</div>
            </div>
            """, unsafe_allow_html=True)

load_css_with_background()

st.title("MoodieFlix 🍿")
st.markdown("Tell me what kind of movie you want, and I'll recommend the perfect one!")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

prompt = st.text_input(
    "What Do you want to watch?",
    placeholder="e.g., I want a romantic comedy with a strong female lead",
    key="movie_input"
)

def get_recommendation(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://moodieflix.streamlit.app",
        "X-Title": "MoodieFlix Recommender"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": """You're a movie expert. Recommend 6-7 movies based on user requests. Format with movie titles in bold using **Movie Title** and include brief descriptions after each title. Each movie should be clearly separated."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

if prompt:
    with st.spinner("Finding your perfect movie... 🎬"):
        recommendation = get_recommendation(prompt)
        movies = parse_movies(recommendation)
        
        st.markdown("---")
        display_cards(movies)
        
        if not movies:
            st.markdown(f'<div class="movie-card"><div class="movie-description">{recommendation}</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("*Want another recommendation? Just enter a new request above!*")