# How to Test Images with Your CNN Model

## ✅ Quick Start - Test a Random Image

Simply run:
```bash
python scripts/test_image.py
```

This will:
- Pick a random image from your dataset
- Show which disease it predicts
- Display confidence percentage
- Show probability bars for all classes

## 📸 Test a Specific Image

To test your own image:
```bash
python scripts/test_image.py path/to/your/image.jpg
```

Example:
```bash
python scripts/test_image.py data/rice_leaf_diseases/leaf_scald/leaf_scald-72-_jpg.rf.dac0829e4d3c23c4344d646105f8121c.jpg
```

## 📊 Understanding the Results

The output shows:
- **Predicted Disease**: The disease the model thinks it is
- **Confidence**: How sure the model is (0-100%)
- **All Probabilities**: Breakdown for each disease class with visual bars

### Example Output:
```
>> PREDICTION RESULTS
============================================================

>> Predicted Disease: LEAF SCALD
>> Confidence: 100.00%

>> All Probabilities:
  bacterial_leaf_blight     [--------------------------------------------------]   0.00%
  brown_spot                [--------------------------------------------------]   0.00%
  leaf_scald                [##################################################] 100.00% <- PREDICTED

============================================================
[OK] Confidence above threshold (60%)
```

## 🎯 Disease Classes

Your model can detect these 3 rice leaf diseases:
1. **Bacterial Leaf Blight**
2. **Brown Spot**
3. **Leaf Scald**

## 📁 Available Test Images

You have 40+ test images in:
```
data/rice_leaf_diseases/
├── bacterial_leaf_blight/
├── brown_spot/
└── leaf_scald/
```

## ⚙️ Model Information

- **Model**: Custom CNN (51.6 million parameters)
- **Input Size**: 224x224 pixels
- **Confidence Threshold**: 60%
- **Model File**: `models/crop_disease_model.pth` (197 MB)

## 💡 Tips

- Images are automatically resized to 224x224
- Works with JPG/JPEG formats
- Model runs on CPU (no GPU needed)
- If confidence is below 60%, consider expert verification
