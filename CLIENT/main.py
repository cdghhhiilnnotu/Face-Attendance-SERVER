from packages_import import *

dataset_path = 'datasets'
class_id = 'TH5216_20CN3'
img_path = 'imgs'

# download_dataset_by_class(dataset_path,class_id)

# cleaning_dataset(dataset_path,'haarcascade_frontalface_default.xml')

# augmentation_dataset_main(dataset_path)

# standardized_image(dataset_path)

split_folder(dataset_path, img_path)

students, student_classes = data_classify(dataset_path, img_path)

train_ds, val_ds, test_ds = augmentation_dataset_extra(img_path)

model = compile_model(student_classes)

fit_model(model, train_ds, val_ds, 'model1.keras')
evaluate_model(model, 'model1.keras', test_ds)

