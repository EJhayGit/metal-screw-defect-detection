import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os
import numpy as np

BATCH_SIZE = 32
IMG_SIZE = (224, 224)
EPOCHS = 10

def build_model():
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False # Freeze base model
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')])
    return model

def calculate_f1_score(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def main():
    # Example relative path where user should drop 'Normal' and 'Defective' images
    dataset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'merged')
    
    if not os.path.exists(dataset_dir):
        print(f"Error: Training dataset not found at {dataset_dir}")
        print("Please place 'Normal' and 'Defective' folders containing merged screw imagery in the datasets/merged/ directory.")
        return
        
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )

    val_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )

    model = build_model()
    
    # Save model.h5 to backend directory
    backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
    os.makedirs(backend_dir, exist_ok=True)
    keras_model_path = os.path.join(backend_dir, 'model.h5')

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=keras_model_path,
            save_best_only=True,
            monitor='val_accuracy'
        ),
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    ]

    print("Starting Model Training for Metal Screw Defect Classification...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=callbacks
    )
    
    # Evaluate Validation Set
    val_loss, val_accuracy, val_precision, val_recall = model.evaluate(val_generator)
    
    f1_score = calculate_f1_score(val_precision, val_recall)
    
    print(f"\n--- Evaluation Results ---")
    print(f"Validation Accuracy: {val_accuracy:.4f} (Target > 0.90)")
    print(f"Validation F1-Score: {f1_score:.4f} (Target > 0.90)")
    # Assume False alarm is 1 - Precision (False Discovery Rate) roughly
    false_alarm_rate = 1.0 - val_precision
    print(f"Estimated False-Alarm Rate: {false_alarm_rate:.4f} (Target < 0.10)")
    
    print(f"\nModel saved to {keras_model_path}")

if __name__ == '__main__':
    main()
