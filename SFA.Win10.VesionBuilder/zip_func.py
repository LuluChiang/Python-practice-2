import zipfile

def fileunzip(fp):
# input: fp: file path like "C:/archive.zip"
    zp = zipfile.ZipFile(fp, "r")
    zp.extractall()
    zp.close()
    return

def filezip(src_path, des_zip):
    # zp = zipfile.ZipFile("archive_install.zip","w")
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         ziph.write(os.path.join(root, file), 
    #                    os.path.relpath(os.path.join(root, file), 
    #                                    os.path.join(path, '..')))
    # ...
    # ...
    return

