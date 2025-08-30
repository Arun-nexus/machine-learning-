import cv2
import streamlit as st
from animalCnnDay3 import safe_generate
from PIL import Image

st.title("animal classifier model")

option = st.radio("chooose an input method: ",["upload image","use webcam"])

if option == "upload image":
    uploaded = st.file_uploader("upload an image", type=["jpg","jpeg","png"])
    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img,caption="uploaded image",use_container_width=True)
        if st.button("predict"):
            species,desc = safe_generate(img)
            st.success(f"this image is looking like : {species}")
            st.info(desc)

elif option == "use webcam":
    run = st.checkbox("open webcam")
    if run:
        cam = cv2.VideoCapture(0)
        ret,frame = cam.read()
        if ret:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            st.image(frame,channels="RGB")
            img = Image.fromarray(frame)
            if st.button("predict from webcam"):
                species,desc = safe_generate(img)
                st.success(f"this image is looking like : {species}")
                st.info(desc)
    cam.release()