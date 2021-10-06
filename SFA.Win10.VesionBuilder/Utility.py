
from datetime import datetime
import os

from io import BytesIO 
import hashlib
import pycdlib

PATH_LOG = "debug.txt"
PATH_CONFIG = "config.ini"


def GetKeyValueinConfig(key, section):
# Example of config file
# [section]
# key=value
#
# input:    key: str
#           section: str
#
    try:
        value = None
        inRightSection = False
        if os.path.isfile(PATH_CONFIG):
            with open(PATH_CONFIG, "r") as config:
                list_config = config.readlines()
                for line in list_config:
                    if line[0] == "#":
                        continue
                    elif line[0] == "[":
                        section_end = line.find("]")
                        if section == line[1:section_end]:
                            inRightSection = True
                        else:
                            inRightSection = False
                    elif line.find(key) == 0 and inRightSection:
                        line = line.strip()
                        value = line[line.find("=") + 1:]               
        else:           
            Dbg_print("Find no config.ini")  
        return value
    except Exception as e:
        Dbg_print("GetKeyValueinConfig(): Err" )

def DeleteTargetFileinConfig(section):
# Example of config file
# [section]
# file path in relative path
#
# input:    section: str
# output:   value: str, as key's value
#
    try:
        inRightSection = False
        if os.path.isfile(PATH_CONFIG):
            with open(PATH_CONFIG, "r") as config:
                list_config = config.readlines()
                for line in list_config:
                    if line[0] == "#" or line[0] == "\n":
                        continue
                    elif line[0] == "[":
                        section_end = line.find("]")
                        if section == line[1:section_end]:
                            inRightSection = True
                        else:
                            inRightSection = False       
                    elif inRightSection:
                        filepath = line[:-1]
                        if os.path.isfile(filepath):
                            utDeleFile(filepath)
                        elif os.path.isdir(filepath):
                            utDeleFilesinFolder(filepath)
                        else:
                            Dbg_print("Target delete file is not found")      
        else:           
            Dbg_print("Find no config.ini") 
        return 
    except Exception as e:
        Dbg_print("DeleteTargetFileinConfig(): Err")


def GetValueFromAttributeName(element, attr_name):
# element: <tag Attribute_name = "Attribute_value"> String </tag> :
# Ex tag: <p Version = "1.300.2467"> Hello </p>
#
# input:    element: string, a element in a xml
#           attr_name: string, target attribute in the element
# return:   attr_val: string,  value of "ApplicationVersion"
#
    idx_name = element.find(attr_name)
    left_DQuote = element.find("\"", idx_name)
    right_DQuote = element.find("\"", left_DQuote + 1)
    attr_val = element[left_DQuote + 1:right_DQuote]
    return attr_val


def Dbg_print(debug_line):
# input: debug_line as string
    now = datetime.now()
    str_datetime = now.strftime("%m/%d %H:%M:%S ")
    with open(PATH_LOG, "a") as fpDbg:
        fpDbg.write(str_datetime + debug_line + "\n")
    

def utDeleLog():
    utDeleFile(PATH_LOG)

def utDeleFile(path):
    if os.path.isfile(path):
        os.remove(path)

# TODO: cant remove folder in a folder yet
def utDeleFilesinFolder(path):
    if os.path.isdir(path):
        for file in os.listdir(path):
            utDeleFile(path + file)

def utMkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

# ***********************
# build ISO function: pycdlib
# ***********************
def utISO_add_file(iso, path):
    iso.add_file(path, "/" + path)


def utISO_add_folder(iso, folder_path, des_path = None):   
    try:
        if des_path is None:
            des_path = "/"
        else:
            des_path += "/"

        files = os.listdir(folder_path + des_path)
        for file in files:
            file_path = folder_path + des_path + file
            if os.path.isdir(file_path):
                iso.add_directory(des_path + file)
                utISO_add_folder(iso, folder_path, des_path + file)
            elif os.path.isfile(file_path):
                iso.add_file(file_path, des_path + file)
            else:
                Dbg_print("File err: " + file_path)
    except Exception as e:
        Dbg_print("utISO_add_folder(): Err" )


def utBuildFolderToISO(tar_path, iso_name):
# Build target path into a ISO file
# input: tar_path: Ex: "bin"
    try:
        if not os.path.isdir(tar_path):
            Dbg_print("utBuildFolderToISO(): " + tar_path + " is not a folder.")
            return
        iso = pycdlib.PyCdlib()
        iso.new(interchange_level = 4) 
        # Level 1: File names are limited to eight characters with a three-character extension. 
        # Directory names are limited to eight characters. Files may contain one single file section.

        utISO_add_folder(iso, tar_path)
        iso.write(iso_name + ".iso")
        iso.close()
        Dbg_print("Build "+ iso_name + ".iso to: " + tar_path)
    except Exception as e:
        Dbg_print("utBuildFolderToISO(): Err")


# ***********************
# SHA256 Function
# ***********************
def SHA256_String(sha256, strTemp):    
    strTemp = str(strTemp).encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(strTemp)
    return sha256



# sha256 = hashlib.sha256()
# Folder_path = "SFA_Win10_Install_/"#"bin2/"

# files = os.listdir(Folder_path)
# for file in files:
#         print(file)
#         sha256 = SHA256_String(sha256, file)
#         print(sha256.hexdigest())
#         with open(Folder_path + file, "rb") as fp:
#             bfile = fp.read()   #read entire file as bytes
#             sha256.update(bfile)
#             print(sha256.hexdigest())

