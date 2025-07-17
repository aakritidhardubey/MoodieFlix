import streamlit as st
import requests

st.set_page_config(page_title="🎬 MoodieFlix 🍿", page_icon="🎥")
st.title("🎥 MoodieFlix")
st.markdown("Tell me what kind of movie you want, and I'll recommend the perfect one!")


OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]


prompt = st.text_input(
    "What Do you want to watch ?",
    placeholder="e.g., I want a romantic comedy with a strong female lead",
)

# LLM Call using OpenRouter
def get_movie_recommendation(prompt):
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
                "content": "You're a movie expert. Recommend movies based on user mood, genre preferences, or emotional needs. Be friendly and concise."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {e}"

if prompt:
    with st.spinner("Finding your perfect movie... 🎬"):
        recommendation = get_movie_recommendation(prompt)
        st.markdown(recommendation)
