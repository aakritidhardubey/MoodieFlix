import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="Movie Recommender", layout="centered")
model=SentenceTransformer('all-MiniLM-L6-v2')

movies=pd.read_csv("tmdb_5000_movies.csv")

movies['combined']=movies['title'] + " - " + movies['overview'].fillna('')

st.title("Movie Recommendation")
user_input= st.text_input("What Do you feel like Watching ?")

movie_embeddings= model.encode(movies['combined'].tolist(), convert_to_tensor=True) 

if user_input:
    query_embedding=model.encode(user_input,convert_to_tensor=True)
    scores=util.cos_sim(query_embedding,movie_embeddings)[0]

    st.write("🔍 Searching for movies that match your vibe...")

    top_indices=scores.argsort(descending=True)[:5]
    st.subheader("🎥 Recommended Movies:")

    for idx in top_indices:
        st.write(f"**{movies.iloc[idx]['title']}** - {movies.iloc[idx]['overview']}")
    
