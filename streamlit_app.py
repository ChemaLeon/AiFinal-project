import streamlit as st
import openai

st.title("CookSmart", text_alignment="center")

col1, col2, col3 = st.columns(3)
with col2:
    st.write("Cook Smarter Not Harder ")