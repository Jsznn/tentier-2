import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Analisis Sentimen Produk",
    page_icon="🛍️",
    layout="centered"
)

# Define pages
page_1 = st.Page("page_1.py", title="Analisis Manual")
page_2 = st.Page("page_2.py", title="Analisis Tokopedia", icon="🛒")

# Navigation
pg = st.navigation([page_1, page_2])

# Run navigation
pg.run()
