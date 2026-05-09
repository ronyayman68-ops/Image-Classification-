import streamlit as st
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="EngineerSupport AI", layout="centered")

# --- AI MODEL LOADING ---
@st.cache_resource
def load_support_model():
    # BART-Large is the "Gold Standard" for accuracy in text classification
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_support_model()

# --- UI HEADER ---
st.title("Technical Ticket Classifier")
st.write("Route development issues to the correct department instantly.")

# --- INPUT SECTION ---
track_text = st.text_area(
    "Describe the technical issue / وصف المشكلة التقنية:", 
    placeholder="e.g., The PySpark job is failing with a memory overflow error..."
)

# Professional Technical Categories based on your stack
departments = [
    "Database & SQL", 
    "Frontend (React/UI)", 
    "Backend (Node.js/ASP.NET)", 
    "Data Engineering (Spark/ETL)"
]

if st.button("Classify Track"):
    if track_text:
        with st.spinner('Analyzing architecture...'):
            results = classifier(track_text, candidate_labels=departments)
        
        st.divider()
        st.subheader("Routing Results / نتائج التوجيه")
        
        # Display the primary department
        top_dept = results['labels'][0]
        top_score = results['scores'][0]
        
        st.success(f"**Recommended Team:** {top_dept} ({top_score*100:.1f}%)")
        
        # Full breakdown for the dashboard
        for i in range(len(results['labels'])):
            label = results['labels'][i]
            score = results['scores'][i]
            st.write(f"{label}")
            st.progress(score)
    else:
        st.warning("Please enter ticket details.")

st.caption("Developed by Rawan Ayman Saber | Data Engineer & Full-Stack Developer")