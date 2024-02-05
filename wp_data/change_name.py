import os
import shutil

def rename_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name == "readme.md":
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, "page.md")
                shutil.move(old_path, new_path)
                print(f"重命名文件：{old_path} -> {new_path}")

def traverse_folders(folder_path):
    path_list = []
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            path_list.append(os.path.join(root, dir_name))
    return path_list

if __name__=='__main__':
    path_list = traverse_folders('./')
    for path_one in path_list:
        rename_files(path_one)