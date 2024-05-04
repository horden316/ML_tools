import xml.etree.ElementTree as ET
import os

def convert_voc_to_yolo(voc_dir, yolo_dir, classes):
    if not os.path.exists(yolo_dir):
        os.makedirs(yolo_dir)

    for xml_file in os.listdir(voc_dir):
        if xml_file.endswith('.xml'):
            tree = ET.parse(os.path.join(voc_dir, xml_file))
            root = tree.getroot()

            txt_filename = os.path.splitext(xml_file)[0] + '.txt'
            with open(os.path.join(yolo_dir, txt_filename), 'w') as txt_file:
                for member in root.findall('object'):
                    cls = member.find('name').text
                    if cls not in classes:
                        continue
                    cls_id = classes.index(cls)

                    bndbox = member.find('bndbox')
                    xmin = float(bndbox.find('xmin').text)
                    xmax = float(bndbox.find('xmax').text)
                    ymin = float(bndbox.find('ymin').text)
                    ymax = float(bndbox.find('ymax').text)

                    x_center = (xmin + xmax) / 2.0
                    y_center = (ymin + ymax) / 2.0
                    width = xmax - xmin
                    height = ymax - ymin

                    img_width = int(root.find('.//size/width').text)
                    img_height = int(root.find('.//size/height').text)

                    x_center /= img_width
                    y_center /= img_height
                    width /= img_width
                    height /= img_height

                    txt_file.write(f'{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')

# 類別列表，例如 ['person', 'car', ...]
classes_list = ['helmet','head','person']

# 將 'voc_dir' 設為的 VOC 檔案目錄，'yolo_dir' 設為存放轉換後檔案的目錄
convert_voc_to_yolo('', '', classes_list)
