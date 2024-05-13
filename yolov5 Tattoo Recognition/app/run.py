from flask import Flask, render_template, request, jsonify
import os
import torch
import clip
from PIL import Image
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Path to the folder containing tattoo images
IMAGE_FOLDER = ''

IMAGE_FOLDER = 'static/images'

@app.route('/')
def index():
    try:
        # List all image files in the IMAGE_FOLDER
        image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    except Exception as e:
        # If there's an error, display it on the page
        return f"Error accessing image directory: {e}"
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tattoo Gallery</title>
   <style>
                #gallery {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px; /* Adjust the space between images */
                    justify-content: center;
                }
                #gallery img {
                    width: 150px; /* Adjust the width of images */
                    height: 200px;
                    cursor: pointer;
                    border: 1px solid #ccc; /* Optional border */
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Optional shadow */
                }
                figure {
                    margin: 0; /* Remove default margin from figure */
                }
                figcaption {
                    text-align: center;
                    font-size: 0.9em; /* Adjust caption font size */
                }
            </style>
        </head>
        <body>
            <h1>Tattoo Gallery</h1>
            <div id="gallery">
                {% for image in images %}
                    <figure>
                        <img src="{{ url_for('static', filename='images/' + image) }}" alt="{{ image }}" onclick="describeImage('{{ image }}')">
                        <figcaption>{{ image }}</figcaption>
                    </figure>
                {% endfor %}
            </div>
            <div id="description"></div>

            <script>
                function describeImage(imageName) {
                    fetch('/describe', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({imageName}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('description').innerText = data.description;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('description').innerText = 'Error fetching description';
                    });
                }
            </script>
        </body>
        </html>
    ''', images=image_files)

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_descriptions(image_path):
    """
    Use CLIP to generate a description of the tattoo.
    """
    # Preprocess the image
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Generate the text prompts you want CLIP to compare the image with.
    # For tattoos, we might have a fixed set of descriptions or generate them dynamically.
    text_descriptions = [
        "a dragon tattoo", "a tribal tattoo", "a floral tattoo",
        "an abstract tattoo", "a geometric tattoo", "an animal tattoo",
        "a lettering tattoo", "a portrait tattoo", "a skull tattoo",
        "a minimalist tattoo"
    ]
    text = clip.tokenize(text_descriptions).to(device)
    
    # Calculate features
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
    # Pick the top result by calculating similarities
    similarities = (image_features @ text_features.T).softmax(dim=-1)
    top_prob, top_idx = similarities[0].topk(1)
    
    # Return the most similar description
    return f"This tattoo is most likely: {text_descriptions[top_idx]}, with a confidence of {top_prob.item():.2f}."


@app.route('/describe', methods=['POST'])
def describe():
    """
    Route to handle the description request.
    """
    image_name = request.json['imageName']
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    description = get_image_descriptions(image_path)
    return jsonify(description=description)

if __name__ == '__main__':
    app.run(debug=True)
