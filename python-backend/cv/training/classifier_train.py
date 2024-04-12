from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
import datetime

import os
import shutil
from sklearn.model_selection import train_test_split

import tensorflow as tf

if tf.test.gpu_device_name():
    print("gpu: {}".format(tf.test.gpu_device_name()))
else:
    print("no gpu for tf")

def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
source_dir = r'C:\Users\Sehap\Documents\code\GagarinHack-2\python-backend\cv\training\classifier\source'
base_dir = os.path.dirname(source_dir)
train_dir = os.path.join(base_dir, 'train')
valid_dir = os.path.join(base_dir, 'valid')
test_dir = os.path.join(base_dir, 'test')

early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, restore_best_weights=True)
model_checkpoint = ModelCheckpoint(filepath='best_model.keras', monitor='val_loss', save_best_only=True)

create_dir_if_not_exists(train_dir)
create_dir_if_not_exists(valid_dir)
create_dir_if_not_exists(test_dir)

train_size = 0.8
valid_size = 0.1
test_size = 0.1

for class_dir in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_dir)
    
    create_dir_if_not_exists(os.path.join(train_dir, class_dir))
    create_dir_if_not_exists(os.path.join(valid_dir, class_dir))
    create_dir_if_not_exists(os.path.join(test_dir, class_dir))
    
    files = [os.path.join(class_path, f) for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
    
    train_files, rest_files = train_test_split(files, test_size=1 - train_size, random_state=42)
    valid_files, test_files = train_test_split(rest_files, test_size=test_size / (test_size + valid_size), random_state=42)
    
    def copy_files(files, dest_dir):
        for f in files:
            shutil.copy(f, os.path.join(dest_dir, os.path.basename(f)))
    
    copy_files(train_files, os.path.join(train_dir, class_dir))
    copy_files(valid_files, os.path.join(valid_dir, class_dir))
    copy_files(test_files, os.path.join(test_dir, class_dir))
image_size = (224, 224)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

valid_generator = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=image_size + (3,))
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

inputs = Input(shape=image_size + (3,))
x = base_model(inputs, training=True)
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
num_classes = len(train_generator.class_indices)
outputs = Dense(num_classes, activation='softmax')(x)

model = Model(inputs, outputs)

model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])


history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=100,
    callbacks=[early_stopping, model_checkpoint, tensorboard_callback]
)

test_loss, test_acc = model.evaluate(test_generator)
print(f'Test accuracy: {test_acc:.3f}, Test loss: {test_loss}')

model_path = r'C:\Users\Sehap\Documents\code\GagarinHack-2\python-backend\cv\models\classifier.keras'
model.save(model_path)
