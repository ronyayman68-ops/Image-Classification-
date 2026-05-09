import streamlit as st
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="VibeCheck | Genre Classifier", layout="centered")

# --- AI MODEL LOADING ---
@st.cache_resource
def load_zero_shot():
    # This model can classify text into ANY labels you give it
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_zero_shot()

# --- UI HEADER ---
st.title("🎵 Music Genre Classifier")
st.write("Enter lyrics or a song description to identify the genre.")

# --- INPUT AREA ---
text_input = st.text_area("Song Lyrics / Description:", placeholder="e.g., Neon lights and synthesizers playing in the midnight rain...")

# Labels you want the AI to choose from
genre_labels = ["Rock", "Hip Hop", "Electronic", "Jazz", "Classical", "Pop"]

if st.button("Classify Genre"):
    if text_input:
        with st.spinner('Analyzing vibes...'):
            res = classifier(text_input, candidate_labels=genre_labels)
            
        st.divider()
        st.subheader(":نتائج التصنيف") # Keeping your Arabic header style
        
        # Show top 3 results
        for i in range(3):
            label = res['labels'][i]
            score = res['scores'][i]
            
            st.write(f"**{label}: {score*100:.2f}%**")
            st.progress(score)
    else:
        st.warning("Please enter some text first.")

st.caption("Built for Rawan's Portfolio")