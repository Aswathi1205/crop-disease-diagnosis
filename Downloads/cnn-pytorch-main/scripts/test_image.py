"""
Simple script to test a single image with the trained crop disease model.

Usage:
    python scripts/test_image.py <path_to_image>
    
    Or run without arguments to test a random image from the dataset.
"""

import sys
import os
import json
import torch
import random
from pathlib import Path
from PIL import Image

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import CropDiseaseClassifier
from src.transforms import ImageTransformer


def test_image(image_path=None):
    """Test a single image with the model."""
    
    base_dir = Path(__file__).parent.parent
    
    # Load configuration
    config_path = base_dir / 'config' / 'model_config.json'
    class_names_path = base_dir / 'config' / 'class_names.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    with open(class_names_path, 'r') as f:
        class_names = json.load(f)['classes']
    
    # Load model
    model_path = base_dir / config['model']['model_path']
    model = CropDiseaseClassifier(num_classes=config['model']['num_classes'])
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    
    # If no image path provided, pick a random one from the dataset
    if image_path is None:
        data_dir = base_dir / 'data' / 'rice_leaf_diseases'
        all_images = list(data_dir.glob('**/*.jpg')) + list(data_dir.glob('**/*.JPG'))
        
        if not all_images:
            print("[X] No images found in data/rice_leaf_diseases/")
            return
        
        image_path = random.choice(all_images)
        print(f"[*] Testing random image: {image_path.name}")
        print(f"[*] From folder: {image_path.parent.name}")
    else:
        image_path = Path(image_path)
        if not image_path.exists():
            print(f"[X] Image not found: {image_path}")
            return
        print(f"[*] Testing image: {image_path.name}")
    
    print("-" * 60)
    
    # Load and display image info
    try:
        image = Image.open(image_path)
        print(f"[OK] Image loaded successfully")
        print(f"  Size: {image.size}")
        print(f"  Mode: {image.mode}")
    except Exception as e:
        print(f"[X] Failed to load image: {e}")
        return
    
    # Transform image
    transformer = ImageTransformer(
        target_size=tuple(config['model']['input_size']),
        mean=config['preprocessing']['mean'],
        std=config['preprocessing']['std']
    )
    
    transformed = transformer.transform(image)
    input_tensor = transformed.unsqueeze(0)  # Add batch dimension
    
    # Run inference
    print("\n[*] Running inference...")
    with torch.no_grad():
        output = model(input_tensor)
    
    # Get predictions
    probabilities = output[0].numpy()
    predicted_idx = probabilities.argmax()
    predicted_class = class_names[predicted_idx]
    confidence = probabilities[predicted_idx] * 100
    
    # Display results
    print("\n" + "=" * 60)
    print(">> PREDICTION RESULTS")
    print("=" * 60)
    print(f"\n>> Predicted Disease: {predicted_class.upper().replace('_', ' ')}")
    print(f">> Confidence: {confidence:.2f}%")
    
    print(f"\n>> All Probabilities:")
    for i, (class_name, prob) in enumerate(zip(class_names, probabilities)):
        bar_length = int(prob * 50)
        bar = "#" * bar_length + "-" * (50 - bar_length)
        marker = " <- PREDICTED" if i == predicted_idx else ""
        print(f"  {class_name:25s} [{bar}] {prob*100:5.2f}%{marker}")
    
    print("\n" + "=" * 60)
    
    # Check if confidence meets threshold
    threshold = config['inference']['confidence_threshold']
    if confidence / 100 >= threshold:
        print(f"[OK] Confidence above threshold ({threshold*100:.0f}%)")
    else:
        print(f"[!] Confidence below threshold ({threshold*100:.0f}%)")
        print("    Consider getting more expert opinion")
    
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific image
        test_image(sys.argv[1])
    else:
        # Test random image
        print("=" * 60)
        print("CROP DISEASE DIAGNOSIS - IMAGE TESTING")
        print("=" * 60)
        print("\nNo image specified. Testing with a random image from dataset...\n")
        test_image()
