import os
import shutil

src_dataset_path = r'C:\Users\Sehap\Documents\code\GagarinHack-2\cv\tr\classifier'

dst_dataset_path = r'C:\Users\Sehap\Documents\code\GagarinHack-2\cv\tr\clNew'

class_dict = {'pass': 0, 'pts': 1, 'sts1': 2, 'sts2': 3, 'vu1': 4, 'vu2': 5}

for phase in ['train', 'valid', 'test']:
    os.makedirs(os.path.join(dst_dataset_path, phase, 'images'), exist_ok=True)
    os.makedirs(os.path.join(dst_dataset_path, phase, 'labels'), exist_ok=True)

    for class_name, class_index in class_dict.items():
        class_path = os.path.join(src_dataset_path, phase, class_name)
        
        for filename in os.listdir(class_path):
            src_file_path = os.path.join(class_path, filename)
            
            dst_image_path = os.path.join(dst_dataset_path, phase, 'images', filename)
            
            shutil.copy(src_file_path, dst_image_path)
            
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            dst_label_path = os.path.join(dst_dataset_path, phase, 'labels', txt_filename)
            
            with open(dst_label_path, 'w') as label_file:
                label_file.write(str(class_index))