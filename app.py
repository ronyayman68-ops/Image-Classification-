import streamlit as st
from transformers import pipeline
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Image Classification App", layout="centered")

# --- AI MODEL LOADING ---
@st.cache_resource
def load_classifier():
    # Using the Google ViT model as seen in your reference images
    return pipeline("image-classification", model="google/vit-base-patch16-224")

classifier = load_classifier()

# --- UI HEADER ---
st.title("🖼️ Image Classification App")

# --- FILE UPLOADER (Arabic labels) ---
uploaded_file = st.file_uploader("...اختار صورة عشان الموديل يحللها", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المرفوعة", use_container_width=True)
    
    st.write("---")
    st.write("...جاري التحليل")
    
    # Run classification
    with st.spinner('Analysing...'):
        results = classifier(image)
    
    st.subheader(":نتائج التصنيف")
    
    # Display results with blue progress bars
    for result in results:
        label = result['label']
        score = result['score']
        
        st.write(f"**{label}: {score*100:.2f}%**")
        st.progress(score)
        st.write("") 

else:
    st.info("الرجاء رفع صورة لبدء عملية التصنيف")