import tensorflow

model = tensorflow.keras.models.load_model(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\classifier_old.keras')
converter = tensorflow.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tensorflow.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)