import streamlit as st
import tensorflow as tf
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

# Load Model and Tokenizer
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

@st.fragment
def display_header():
    st.title("🛍️ Analisis Sentimen Ulasan Produk")
    st.markdown("Aplikasi ini menggunakan **Deep Learning (LSTM)** untuk memprediksi sentimen dari ulasan produk bahasa Indonesia.")

@st.fragment
def display_input_and_result(model, tokenizer):
    # Input Section
    st.subheader("Masukkan Ulasan")
    review_text = st.text_area(
        "Tulis ulasan produk di sini:",
        height=150,
        placeholder="Contoh: Barang sangat bagus, pengiriman cepat, saya sangat puas!"
    )

    if st.button("Analisis Sentimen"):
        if review_text.strip():
            with st.spinner('Menganalisis...'):
                try:
                    # Preprocessing
                    max_len = 100 # Must match the training max_len
                    sequences = tokenizer.texts_to_sequences([review_text])
                    padded = pad_sequences(sequences, maxlen=max_len)
                    
                    # Prediction
                    prediction = model.predict(padded)
                    
                    # Interpret result
                    output_shape = model.output_shape
                    
                    sentiment = ""
                    confidence = 0.0
                    
                    # Binary Classification (Sigmoid)
                    if output_shape[-1] == 1:
                        score = prediction[0][0]
                        sentiment = "Positif" if score > 0.5 else "Negatif"
                        confidence = score if score > 0.5 else 1 - score
                    
                    # Multiclass Classification (Softmax)
                    else:
                        class_idx = np.argmax(prediction)
                        confidence = np.max(prediction)
                        
                        # Mapping classes (Assuming alphabetical order from LabelEncoder)
                        if output_shape[-1] == 2:
                            classes = ['Negatif', 'Positif']
                        elif output_shape[-1] == 3:
                            classes = ['Negatif', 'Netral', 'Positif']
                        else:
                            classes = [f'Kelas {i}' for i in range(output_shape[-1])]
                            
                        if class_idx < len(classes):
                            sentiment = classes[class_idx]
                        else:
                            sentiment = f"Kelas {class_idx}"

                    # Display Result
                    st.markdown("---")
                    st.subheader("Hasil Analisis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Sentimen", sentiment)
                    
                    with col2:
                        st.metric("Confidence Score", f"{confidence:.2%}")
                    
                    # Visual Feedback
                    if sentiment.lower() == "positif":
                        st.success("Ulasan ini bernada **Positif**! 😄")
                        st.balloons()
                    elif sentiment.lower() == "negatif":
                        st.error("Ulasan ini bernada **Negatif**. 😔")
                    else:
                        st.info(f"Ulasan ini bernada **{sentiment}**.")
                        
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        else:
            st.warning("Mohon masukkan teks ulasan terlebih dahulu.")


def display_sidebar():
    st.sidebar.title("Tentang")
    st.sidebar.info(
        "Aplikasi ini didukung oleh model LSTM yang dilatih menggunakan dataset PRDECT-ID."
    )

def main():
    # Custom CSS
    st.markdown("""
    <style>
        .stTextArea textarea {
            font-size: 16px;
        }
        .stButton button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    try:
        model, tokenizer = load_assets()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat model: {e}")
        st.info("Pastikan Anda telah menjalankan notebook `nlp.ipynb` untuk melatih dan menyimpan model.")
        st.stop()

    display_header()
    display_input_and_result(model, tokenizer)
    display_sidebar()

if __name__ == "__main__":
    main()
