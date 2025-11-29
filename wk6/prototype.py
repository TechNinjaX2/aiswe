# Lightweight Image Classification with TensorFlow + TFLite
# Example: Recognizing recyclable items

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

# -----------------------------
# 1. Prepare a sample dataset
# -----------------------------
# For demonstration, we'll use a small subset of CIFAR-10
# (you can replace it with your own recyclable items dataset)
from tensorflow.keras.datasets import cifar10

# Load dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# For simplicity, select only 3 classes to simulate recyclables:
# e.g., 0: airplane, 1: automobile, 2: bird
selected_classes = [0, 1, 2]

train_filter = np.isin(y_train, selected_classes).flatten()
test_filter = np.isin(y_test, selected_classes).flatten()

x_train, y_train = x_train[train_filter], y_train[train_filter]
x_test, y_test = x_test[test_filter], y_test[test_filter]

# Normalize images
x_train, x_test = x_train / 255.0, x_test / 255.0

# -----------------------------
# 2. Build a lightweight model
# -----------------------------
model = models.Sequential([
    layers.Input(shape=(32, 32, 3)),
    layers.Conv2D(16, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(selected_classes), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# -----------------------------
# 3. Train the model
# -----------------------------
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

# -----------------------------
# 4. Evaluate the model
# -----------------------------
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {test_acc:.2f}")

# -----------------------------
# 5. Convert to TensorFlow Lite
# -----------------------------
tflite_model = tf.lite.TFLiteConverter.from_keras_model(model).convert()

# Save TFLite model
tflite_model_path = "recyclable_model.tflite"
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

print(f"TFLite model saved to {tflite_model_path}")

# -----------------------------
# 6. Test TFLite model
# -----------------------------
# Load TFLite model
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test on a single sample
sample_image = np.expand_dims(x_test[0], axis=0).astype(np.float32)

interpreter.set_tensor(input_details[0]['index'], sample_image)
interpreter.invoke()
prediction = interpreter.get_tensor(output_details[0]['index'])
predicted_class = np.argmax(prediction)

print(f"Predicted class: {predicted_class}, True class: {y_test[0][0]}")

# -----------------------------
# 7. Edge AI Benefits
# -----------------------------
"""
Edge AI allows running models directly on devices like smartphones, cameras, or IoT gadgets without relying on the cloud. 
Benefits for real-time applications:
1. Low Latency: Instant inference without network delay.
2. Privacy: Data stays on the device, reducing exposure risk.
3. Offline Operation: Works without internet.
4. Reduced Bandwidth: Less need to send data to the cloud.

This TFLite model can now be deployed on phones or microcontrollers for real-time recyclable item recognition.
"""
