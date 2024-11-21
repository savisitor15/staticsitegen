import os
import shutil

def copy_files(files: list[str], dest_path:str) -> bool:
    """Empty the destination directoy"""
    if len(files) == 0:
        return True
    shutil.copy(files[0], os.path.join(dest_path))
    return copy_files(files[1:], dest_path)


def update_files(source_path:str, dest_path:str) -> list[str]:
    source_files = []
    source_pw = os.path.join(os.path.curdir,source_path)
    if os.path.exists(os.path.join(os.path.curdir,source_path)):
        source_files = [os.path.join(source_pw,x) for x in os.listdir(source_pw) if os.path.isfile(os.path.join(source_pw,x))]
    else:
        raise FileNotFoundError("Source directory missing!")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        # recreate the folder
        os.mkdir(dest_path)
    if len(source_files) > 0:
        if not copy_files(source_files, dest_path):
            raise Exception("Error copying files to destination")
    return source_files

    
