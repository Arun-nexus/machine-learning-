import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
from transformers import pipeline
import cv2
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

generator = None
try:
    gen_device = 0 if device.type == "cuda" else -1
    generator = pipeline("text-generation", model="gpt2", device=gen_device,truncation=True)
    print("Generator ready. Device:", gen_device)
except Exception as e:
    print("Warning: generator pipeline could not be created:", e)
    generator = None

file_path = r"C:\Users\Arun\Downloads\translation.json"
with open(file_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

key_pair = list(dictionary.keys())

num_classes = 151
model = models.vgg19(weights=None)
model.classifier[6] = nn.Linear(4096, num_classes)

weights_path = r"C:\Users\Arun\Downloads\animal_cnn_vgg19 (1).pth"


sd = torch.load(weights_path, map_location=device)

if isinstance(sd, dict):
        if 'state_dict' in sd:
            sd = sd['state_dict']
        elif 'model_state_dict' in sd:
            sd = sd['model_state_dict']
try:
        # Attempt strict load first
        model.load_state_dict(sd)
        print("State dict loaded (strict=True).")
except RuntimeError as e:
        print("Strict load failed:", e)
        res = model.load_state_dict(sd, strict=False)
        print("Loaded with strict=False. Missing keys:", res.missing_keys, "Unexpected keys:", res.unexpected_keys)

model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

if num_classes != len(key_pair):
    print(f"num_classes ({num_classes}) is not found ({len(key_pair)}).")

cam = cv2.VideoCapture(0)

ractangle = False
frame = None
ex = ey = ix = iy = -1

def safe_generate(prompt):

    if generator is None:
        return "[Generator unavailable]"
    try:
        out = generator(prompt, max_length=60, num_return_sequences=1)
        return out[0].get("generated_text", str(out))
    except Exception as e:
        return f"[Generation error: {e}]"

def crop(event, x, y, flags, param):
    global ractangle, ex, ey, ix, iy, frame
    if event == cv2.EVENT_LBUTTONDOWN:
        ractangle = True
        ex, ey = x, y
    elif event == cv2.EVENT_MOUSEMOVE and ractangle:
        temp = frame.copy()
        cv2.rectangle(temp, (ex, ey), (x, y), (0, 0, 255), 1)
        cv2.imshow("window", temp)
    elif event == cv2.EVENT_LBUTTONUP:
        ractangle = False
        ix, iy = x, y
        x1, y1 = min(ex, ix), min(ey, iy)
        x2, y2 = max(ex, ix), max(ey, iy)

        if (x2 - x1) < 5 or (y2 - y1) < 5:
            return

        cropped_image = frame[y1:y2, x1:x2]
        if cropped_image.size == 0:
            print("Empty crop; skipping.")
            return

        img = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        tensor = transform(img).unsqueeze(0).to(device)
        tensor = tensor.float()

        with torch.no_grad():
            out = model(tensor)
            _, pred = torch.max(out, 1)
        pred = int(pred.item())

        if 0 <= pred < len(key_pair):
            species = key_pair[pred]
            prompt = f"Describe a {species} in simple words."
            gen_text = safe_generate(prompt)
            print("Predicted:", species, "| Prompt:", prompt)
            print("Generated:\n", gen_text)
        else:
            print("Prediction is an  unknown class.")

        cv2.imshow("crop", cropped_image)

cv2.namedWindow("window")
cv2.setMouseCallback("window", crop)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("window", frame)
        if cv2.waitKey(1) & 0xFF == ord("x"):
            break
finally:
    cam.release()
    cv2.destroyAllWindows()

