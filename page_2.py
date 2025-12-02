import streamlit as st
import tensorflow as tf
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Load Model and Tokenizer (Cached)
@st.cache_resource
def load_assets():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'models', 'sentiment_model.h5')
    tokenizer_path = os.path.join(base_dir, 'models', 'tokenizer.pickle')
    
    if not os.path.exists(model_path) or not os.path.exists(tokenizer_path):
        raise FileNotFoundError("Model or Tokenizer not found. Please run the training notebook first.")

    model = tf.keras.models.load_model(model_path)
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return model, tokenizer

@st.cache_data(show_spinner=False)
def scrape_tokopedia_reviews(url):
    """
    Scrapes reviews from a Tokopedia product URL using Selenium and BeautifulSoup.
    Returns a list of review texts.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    reviews = []
    driver = None
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        
        # Scroll to load reviews (Tokopedia loads reviews dynamically)
        # We'll scroll down a few times
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3): # Scroll 3 times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # Wait for content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # Parse content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Tokopedia reviews often have data-testid="msgReview" or specific classes
        # We'll try data-testid first as it's more stable
        review_elements = soup.find_all(attrs={"data-testid": "msgReview"})
        
        if not review_elements:
            # Fallback: try to find by class if testid fails (classes might change)
            # This is a generic fallback, might need adjustment
            review_elements = soup.find_all('span', {'data-testid': 'msgReview'})
            
        for el in review_elements:
            text = el.get_text().strip()
            if text:
                reviews.append(text)
                
    except Exception as e:
        st.error(f"Error scraping: {e}")
    finally:
        if driver:
            driver.quit()
            
    return reviews[:5] # Return top 5 reviews

@st.fragment
def display_header():
    st.title("🛍️ Tokopedia Review Analyzer")
    st.markdown("Masukkan link produk Tokopedia untuk menganalisis sentimen ulasan secara otomatis (Real-time Scraping).")

@st.fragment
def display_input_section(model, tokenizer):
    product_url = st.text_input("Masukkan URL Produk Tokopedia", placeholder="https://www.tokopedia.com/...")
    
    if st.button("Dapatkan & Analisis Ulasan"):
        if "tokopedia.com" in product_url:
            
            progress_bar = st.progress(0, text="Memulai proses...")
            
            try:
                # Step 1: Scraping
                progress_bar.progress(20, text="Membuka browser & memuat halaman...")
                
                # We use a wrapper to call the cached function but we want to show progress
                # Since the function is cached, subsequent calls won't show progress updates inside the function
                # So we simulate progress for the user experience or rely on the cached result returning instantly
                
                start_time = time.time()
                reviews = scrape_tokopedia_reviews(product_url)
                
                progress_bar.progress(80, text="Ekstraksi data selesai. Menganalisis sentimen...")
                
                if not reviews:
                    st.warning("Tidak ditemukan ulasan atau gagal mengambil data. Pastikan link produk benar dan memiliki ulasan.")
                    progress_bar.empty()
                    return

                st.success(f"Berhasil mengambil {len(reviews)} ulasan!")
                st.subheader("Analisis Sentimen Ulasan")
                
                for i, review in enumerate(reviews):
                    with st.container():
                        st.markdown(f"**Ulasan {i+1}:**")
                        st.info(f"\"{review}\"")
                        
                        # Predict
                        max_len = 100
                        sequences = tokenizer.texts_to_sequences([review])
                        padded = pad_sequences(sequences, maxlen=max_len)
                        prediction = model.predict(padded)
                        
                        output_shape = model.output_shape
                        sentiment = "Unknown"
                        color = "grey"
                        
                        if output_shape[-1] == 1:
                            score = prediction[0][0]
                            sentiment = "Positif" if score > 0.5 else "Negatif"
                        else:
                             # Assuming 2 classes: Negatif, Positif
                            classes = ['Negatif', 'Positif']
                            class_idx = np.argmax(prediction)
                            if class_idx < len(classes):
                                sentiment = classes[class_idx]
                        
                        if sentiment.lower() == "positif":
                            color = "green"
                        elif sentiment.lower() == "negatif":
                            color = "red"
                            
                        st.markdown(f"Sentimen: :{color}[**{sentiment}**]")
                        st.divider()
                
                progress_bar.progress(100, text="Selesai!")
                time.sleep(1)
                progress_bar.empty()
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
                progress_bar.empty()
                        
        elif product_url:
            st.error("URL tidak valid. Harap masukkan link Tokopedia yang benar.")

def main():
    try:
        model, tokenizer = load_assets()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
        
    display_header()
    display_input_section(model, tokenizer)

if __name__ == "__main__":
    main()
