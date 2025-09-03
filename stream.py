import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from transformers import pipeline
from PIL import Image
import streamlit as st
from streamlit_cropper import st_cropper

file_path = r"C:\Users\Arun\Downloads\translation.json"
with open(file_path, "r") as f:
    dictionary = json.load(f)
key_pair = list(dictionary.keys())
num_classes = len(key_pair)

model = models.vgg19(weights=None)
model.classifier[6] = nn.Linear(4096, num_classes)
weights_path = r"C:\Users\Arun\Downloads\animal_cnn_vgg19 (1).pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sd = torch.load(weights_path, map_location=device)
model.load_state_dict(sd, strict=False)
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

gen_device = 0 if torch.cuda.is_available() else -1
generator = pipeline("text-generation", model="distilgpt2", device=gen_device)

def predict_and_generate(img: Image.Image):
    tensor = transform(img).unsqueeze(0).to(device).float()
    with torch.no_grad():
        out = model(tensor)
        _, pred = torch.max(out, 1)
    pred_idx = int(pred.item())
    species = key_pair[pred_idx]

    prompt = f"Describe a {species} in simple words."
    out = generator(prompt, max_new_tokens=40, num_return_sequences=1)
    description = out[0]["generated_text"]
    return species, description

st.title(" Animal Prediction Model")

option = st.radio("Choose input method:", ["Upload Image", "Use Webcam"])

if option == "Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, caption="Uploaded Image", use_container_width=True)
        if st.button("Predict"):
            species, desc = predict_and_generate(img)
            st.success(f"Predicted: {species}")
            st.info(desc)

elif option == "Use Webcam":
    img_file = st.camera_input(" Take a picture")
    if img_file:
        img = Image.open(img_file).convert("RGB")
        st.write("✂️ Select area to crop:")
        cropped_img = st_cropper(img, realtime_update=True, box_color='red', aspect_ratio=None)
        st.image(cropped_img, caption="Cropped Image")
        if st.button("Predict from Webcam"):
            species, desc = predict_and_generate(cropped_img)
            st.success(f"Predicted: {species}")
            st.info(desc)
