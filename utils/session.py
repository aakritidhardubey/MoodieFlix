import streamlit as st

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
