import os
from diff_cards import process_photos_dir

if __name__ == "__main__":

    data_dir = "./data"
    out_dir = "./borders"
    data_dirs = os.listdir(data_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for d in data_dirs:
        in_folder_path = os.path.join(data_dir, d)
        out_file_path = os.path.join(out_dir, os.path.split(os.path.basename(in_folder_path))[1]) + '.png'

        if not os.path.isdir(in_folder_path):
            continue

        print("###########")
        print(in_folder_path, "->", out_file_path)
    
        process_photos_dir(in_folder_path, out_file_path)
