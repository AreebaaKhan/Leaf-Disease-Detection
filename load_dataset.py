##This file is Not necessary NOW
import os
import cv2
import numpy as np

# ── Configuration ──────────────────────────────────────────────
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
IMG_SIZE = (224, 224)

# Label mapping
CLASSES = {
    "healthy":   0,
    "rust":      1,
    "leaf_spot": 2,
    "mildew":    3,
}

# ── Load & preprocess ─────────────────────────────────────────
X = []  # images
y = []  # labels

for class_name, label in CLASSES.items():
    class_dir = os.path.join(DATASET_DIR, class_name)

    if not os.path.isdir(class_dir):
        print(f"[WARNING] Directory not found, skipping: {class_dir}")
        continue

    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)

        try:
            img = cv2.imread(img_path)

            # Skip files that OpenCV could not decode
            if img is None:
                print(f"[SKIP] Could not read (corrupted/unsupported): {img_path}")
                continue

            # Resize to 224×224
            img_resized = cv2.resize(img, IMG_SIZE)

            X.append(img_resized)
            y.append(label)

        except Exception as e:
            print(f"[ERROR] Failed to process {img_path}: {e}")

# ── Convert to NumPy arrays ───────────────────────────────────
X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.int32)

# ── Print dataset summary ─────────────────────────────────────
print("\n══════════════════════════════════════")
print(f"  Images array shape : {X.shape}")   # (N, 224, 224, 3)
print(f"  Labels array shape : {y.shape}")   # (N,)
print(f"  Total samples      : {len(y)}")
print(f"  Classes            : {list(CLASSES.keys())}")
print("══════════════════════════════════════")
