import os
import shutil
import csv

def prepare():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archive_dir = os.path.join(base_dir, 'datasets', 'archive')
    train_csv = os.path.join(archive_dir, 'train.csv')
    train_img_dir = os.path.join(archive_dir, 'train')
    
    dest_dir = os.path.join(base_dir, 'datasets', 'merged')
    normal_dir = os.path.join(dest_dir, 'Normal')
    defective_dir = os.path.join(dest_dir, 'Defective')
    
    os.makedirs(normal_dir, exist_ok=True)
    os.makedirs(defective_dir, exist_ok=True)
    
    if not os.path.exists(train_csv):
        print(f"Error: Could not find {train_csv}")
        return

    count = 0
    with open(train_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fname = row['filename']
            anomaly = int(row['anomaly'])
            src_path = os.path.join(train_img_dir, fname)
            
            if os.path.exists(src_path):
                dest_path = os.path.join(defective_dir if anomaly == 1 else normal_dir, fname)
                shutil.copy2(src_path, dest_path)
                count += 1
            else:
                pass # print(f"Warning: {src_path} not found.") # too much noise
                
    print(f"Dataset successfully organized: Copied {count} files to 'Normal' and 'Defective' folders in datasets/merged/!")

if __name__ == '__main__':
    prepare()
