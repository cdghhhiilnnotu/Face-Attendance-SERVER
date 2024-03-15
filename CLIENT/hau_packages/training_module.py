import os
import splitfolders

import keras
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.applications import DenseNet169

from prepare_module import reset_path

def init_model(input_shape, len_class):
    densenet = DenseNet169(weights="imagenet", include_top=False, input_shape=input_shape)
    densenet.trainable = False
    inputs = keras.Input(input_shape)
    x = densenet(inputs, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(1024, activation='relu')(x)
    x = keras.layers.Dense(len_class, activation='softmax')(x)
    model = keras.Model(inputs, x)

    return model

def split_folder(data_path, imgs_path):
    reset_path('imgs')
    splitfolders.ratio(data_path, output=f'{imgs_path}', seed=123, ratio=(.7,.15,.15), group_prefix=None)

def data_classify(data_path, imgs_path):
    students = []
    for student in os.listdir(data_path):
      students.append([fn for fn in os.listdir(f'{data_path}/{student}')])
    
    student_classes = []
    for i in os.listdir(f'{imgs_path}/train'):
        student_classes+=[i]
    student_classes.sort()

    return students, student_classes

def compile_model(student_classes):
    img_height, img_width = 224,224
    input_shape=(img_height, img_width, 3)

    model = init_model(input_shape, len(student_classes))
    
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    
    model.summary()
    return model

def fit_model(model, train_ds, val_ds, model_name):
    checkpointer = ModelCheckpoint(filepath=f'last_saved_models/{model_name}',
                                   monitor='val_accuracy', mode='max',
                                   verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=2, min_lr=0.001)
    callbacks=[early_stopping, reduce_lr, checkpointer]

    history = model.fit(train_ds, epochs = 100, validation_data = val_ds, callbacks=callbacks)
    return model

def evaluate_model(model, model_name, test_ds):
    model.load_weights(f'last_saved_models/{model_name}')
    score = model.evaluate(test_ds, verbose=1)