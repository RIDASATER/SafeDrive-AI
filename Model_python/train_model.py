import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# =========================
# 📁 Chemin du dossier contenant toutes les données d'entraînement
# =========================
train_dir = 'data/train'  # doit contenir 'open_eyes' et 'closed_eyes'

# =========================
# 🔄 Prétraitement & Augmentation avec validation_split
# =========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True,
    validation_split=0.2  # 20% pour validation
)

# Générateur pour les données d'entraînement
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary',
    color_mode='grayscale',
    subset='training'  # données pour entraînement
)

# Générateur pour les données de validation
val_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary',
    color_mode='grayscale',
    subset='validation'  # données pour validation
)

# =========================
# 🧠 Architecture du modèle CNN
# =========================
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # classification binaire : yeux ouverts ou fermés
])

# =========================
# ⚙️ Compilation du modèle
# =========================
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =========================
# 🎯 Entraînement du modèle
# =========================
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

# =========================
# 💾 Sauvegarde du modèle entraîné
# =========================
model.save('model_drowsiness_detection.h5')
print("Modèle sauvegardé sous model_drowsiness_detection.h5")
