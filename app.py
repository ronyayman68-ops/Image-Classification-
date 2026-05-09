import streamlit as st
from transformers import pipeline
from PIL import Image


st.set_page_config(page_title="Image Classification App", layout="centered")


@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="google/vit-base-patch16-224")

classifier = load_classifier()


st.title("🖼️ Image Classification App")

uploaded_file = st.file_uploader("...اختار صورة عشان الموديل يحللها", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المرفوعة", use_container_width=True)
    
    st.write("...جاري التحليل")
    
    with st.spinner('Analysing...'):
        results = classifier(image)
    
    st.write("---")
    st.subheader(":نتائج التصنيف")
    
    for result in results:
        label = result['label']
        score = result['score']
        percentage = score * 100
        
        st.write(f"**{label}: {percentage:.2f}%**")
        
        st.progress(score)
        st.write("") 

else:
    st.info("الرجاء رفع صورة لبدء عملية التصنيف")