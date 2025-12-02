import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Analisis Sentimen Produk",
    layout="centered"
)

# Define pages
page_1 = st.Page("page_1.py", title="Analisis Sentimen")

# Navigation
pg = st.navigation([page_1])

# Run navigation
pg.run()
