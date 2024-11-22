import os
import shutil

def copy_files(src_path:str, files: list[str], dest_path:str) -> bool:
    """Empty the destination directoy"""
    if len(files) == 0:
        return True
    file_dir = os.path.dirname(files[0])
    if file_dir != "":
        if not os.path.exists(os.path.join(dest_path, file_dir)):
            os.mkdir(os.path.join(dest_path, file_dir))
    shutil.copy(os.path.join(src_path, files[0]), os.path.join(dest_path, file_dir))
    return copy_files(src_path, files[1:], dest_path)

def get_files(source_path:str) -> list[str]:
    raw_files = os.listdir(source_path)
    output = []
    for fl in raw_files:
        if os.path.isfile(os.path.join(source_path, fl)):
            output.append(fl)
        else:
            sub_path = os.path.join(source_path, fl)
            for fl2 in get_files(sub_path):
                if os.path.isfile(os.path.join(sub_path, fl2)):
                    output.append(os.path.join(fl, fl2))
    return output
        

def update_files(source_path:str, dest_path:str) -> list[str]:
    source_files = []
    source_pw = os.path.join(os.path.curdir,source_path)
    if os.path.exists(os.path.join(os.path.curdir,source_path)):
        source_files = get_files(source_pw)
    else:
        raise FileNotFoundError("Source directory missing!")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        # recreate the folder
        os.mkdir(dest_path)
    if len(source_files) > 0:
        if not copy_files(source_path, source_files, dest_path):
            raise Exception("Error copying files to destination")
    return source_files

    
