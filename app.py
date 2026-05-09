import streamlit as st
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="Music Classifier Pro", layout="centered")

# --- AI MODEL LOADING ---
@st.cache_resource
def load_classifier():
    # Zero-shot is perfect here because it understands relationships between artists and genres
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_classifier()

# --- UI HEADER ---
st.title("🎵 Artist & Lyric Classifier")
st.write("Input the artist and lyrics to predict the genre and mood.")

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])

with col1:
    artist_name = st.text_input("Artist Name", placeholder="e.g., Taylor Swift")

with col2:
    lyrics_text = st.text_area("Song Lyrics", placeholder="Enter a few lines here...")

# Define what we want to detect
genres = ["Pop", "Rock", "Hip Hop", "Country", "Jazz", "Electronic"]

if st.button("Analyze Song"):
    if artist_name and lyrics_text:
        # We combine both inputs for better context
        combined_text = f"Artist: {artist_name}. Lyrics: {lyrics_text}"
        
        with st.spinner('Analyzing artist style and lyrics...'):
            results = classifier(combined_text, candidate_labels=genres)
        
        st.divider()
        st.subheader(":نتائج التحليل") # Arabic subheader per your style
        
        # Display results with blue progress bars
        for i in range(3):
            label = results['labels'][i]
            score = results['scores'][i]
            st.write(f"**{label}** ({score*100:.1f}%)")
            st.progress(score)
            
    else:
        st.warning("Please provide both an Artist and some Lyrics.")

st.caption("Developed by Rawan Ayman Saber")