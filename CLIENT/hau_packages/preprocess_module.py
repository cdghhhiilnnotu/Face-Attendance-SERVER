from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2

def tracking_face(img, haar_model= 'haarcascade_frontalface_default.xml'):
    img_faces = []
    img = cv2.resize(img, (int(img.shape[1]/(img.shape[0]/512)),512), interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier(haar_model)
    faces = face_detector.detectMultiScale(img_gray, 1.2, 5)

    for (x, y, w, h) in faces:
        img_faces.append(img[y:y+h, x:x+w])
    return img_faces

def augmentation_dataset_main(data_path):
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.2,
        fill_mode='constant',
        horizontal_flip=True
    )
    
    for className in os.listdir(data_path):
        classPATH = os.path.join(data_path, className)
        len_IMG = len(os.listdir(classPATH))
        for imgName in os.listdir(classPATH):
            imgPATH = os.path.join(classPATH, imgName)
            img = load_img(imgPATH)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)
    
            i = 0
            for batch in datagen.flow(x, batch_size=1, save_to_dir=classPATH, save_prefix=className, save_format='png'):
                i += 1
                if i > int(100/len_IMG):
                    break

def standardized_image(data_path):
    for pattern in os.listdir(data_path):
        pattern_path = os.path.join(data_path,pattern)
        for image in os.listdir(pattern_path):
            image_path = os.path.join(pattern_path, image)
            img = cv2.imread(image_path)
            img = cv2.resize(img, (224,224))
            cv2.imwrite(image_path, img)

def augmentation_dataset_extra(img_path):
    batch_size = 64
    img_height, img_width = 224,224
    datagen = ImageDataGenerator(
        rescale=1./255
    )
    
    train_ds = datagen.flow_from_directory(
        f'{img_path}/train',
        target_size = (img_height, img_width),
        batch_size = batch_size,
        subset = 'training',
        class_mode = 'categorical'
    )
    
    val_ds = datagen.flow_from_directory(
        f'{img_path}/val',
        target_size = (img_height, img_width),
        batch_size = batch_size,
        class_mode = 'categorical',
        shuffle = False
    )
    
    test_ds = datagen.flow_from_directory(
        f'{img_path}/test',
        target_size = (img_height, img_width),
        batch_size = batch_size,
        class_mode='categorical',
        shuffle=False)

    return train_ds, val_ds, test_ds
