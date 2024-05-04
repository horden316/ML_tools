import os
import shutil
import random

def split_data_set(image_dir, yolo_dir, output_base, train_percent=70, val_percent=20, test_percent=10):
    # 檢查比例之和必須為100
    assert train_percent + val_percent + test_percent == 100, "The sum of the percentages must be 100"

    # 創建輸出目錄
    output_dirs = {
        'images': {
            'train': os.path.join(output_base, 'train', 'images'),
            'val': os.path.join(output_base, 'val', 'images'),
            'test': os.path.join(output_base, 'test', 'images'),
        },
        'labels': {
            'train': os.path.join(output_base, 'train', 'labels'),
            'val': os.path.join(output_base, 'val', 'labels'),
            'test': os.path.join(output_base, 'test', 'labels'),
        }
    }
    for sub_dir in output_dirs['images'].values():
        os.makedirs(sub_dir, exist_ok=True)
    for sub_dir in output_dirs['labels'].values():
        os.makedirs(sub_dir, exist_ok=True)

    # 獲取所有圖像檔案
    images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(images)

    # 分割資料集
    total_images = len(images)
    train_end = total_images * train_percent // 100
    val_end = train_end + (total_images * val_percent // 100)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    # 複製檔案到相應的資料夾
    for image_set, subset in zip([train_images, val_images, test_images], ['train', 'val', 'test']):
        for image in image_set:
            # Copy images
            shutil.copy(os.path.join(image_dir, image), output_dirs['images'][subset])
            
            # Copy labels
            label_file = image.replace(os.path.splitext(image)[1], '.txt')
            label_path = os.path.join(yolo_dir, label_file)
            if os.path.exists(label_path):
                shutil.copy(label_path, output_dirs['labels'][subset])


# 圖片目錄和標註目錄路徑，以及輸出基本目錄
image_directory = ''
yolo_annotation_directory = ''
output_directory = ''

split_data_set(image_directory, yolo_annotation_directory, output_directory)
