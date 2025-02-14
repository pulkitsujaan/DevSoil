from flask import Flask, render_template, request, jsonify, url_for, redirect
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import io
import os


app = Flask(__name__)

class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()

        # Convolutional Layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)

        # Pooling Layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fully Connected Layers
        self.fc1 = nn.Linear(128 * 16 * 16, 512)  # Assuming input size is (3, 128, 128)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 5)  # 5 output classes (Black Soil, Cinder Soil, etc.)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # Conv1 -> ReLU -> Pool
        x = self.pool(F.relu(self.conv2(x)))  # Conv2 -> ReLU -> Pool
        x = self.pool(F.relu(self.conv3(x)))  # Conv3 -> ReLU -> Pool

        # Flatten the feature maps
        x = x.view(-1, 128 * 16 * 16)

        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)  # Output layer (logits)

        return x

# Load PyTorch model
model_path = os.path.join("model", "model.pth")
model = CustomCNN()
model.load_state_dict(torch.load("model/model.pth", map_location=torch.device("cpu")))
model.eval()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
    predicted_class = torch.argmax(output, 1).item()

    class_names = ["Alluvial Soil", "Black Soil", "Clay Soil", "Red Soil"]
    prediction = class_names[predicted_class]

    return jsonify({"Soil Type":prediction}) 
    # return redirect(url_for('result'),prediction)


# After prediction results
@app.route("/blacksoil")
def blackSoil():
    return render_template("blacksoil.html")
@app.route("/redsoil")
def redSoil():
    return render_template("redsoil.html")
@app.route("/alluvialsoil")
def alluvialSoil():
    return render_template("alluvialsoil.html")
@app.route("/claysoil")
def claySoil():
    return render_template("claysoil.html")

if __name__ == "__main__":
    app.run(debug=True)
