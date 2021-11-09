# Version: Python 3.9.7 64-bit
# Todo list:
# 1. Calculate SHA256 for authenticate (hard)
# 2. for other customers
#       => select config
# 3. UI optimize 
# 4. catch exception type
# 5. seperate to more step, and set a "one shot" button for build all
# 
#  
# Module used:
# 1. Tkinker: GUI
#     1. Frame
#     2. Button
#     3. Entry
# 2. File IO: import os, import shutil
# 3. String processing
# 4. zipfile: import zipfile, import shutil
# 5. list 
# 6. pycdlib: for building iso
#       https://clalancette.github.io/pycdlib/
#       py -m pip install pycdlib
# 7. pyinstaller: package python project into a exe
#       py -m pip install pyinstaller
#       UPX is not available: UPX is not available, which means pyinstaller can not find upx.exe to encrypt exe file. 
#           In order to fix it, we should download upx. Put upx.1 and upx.exe with this project in same path.
#       Example: "pyinstaller -F ./Hello.py
#
# Issue: 
#   1. line 101: after build to exe, sometimes it crash while calling askopenfilename,

# For GUI
import tkinter as tk 
from tkinter import filedialog
from datetime import datetime

# File processing
import os
import shutil
from tkinter.constants import NSEW

# Others
import Utility
import zip_func


# CONST
COLOR_FRAMEBG_UNDO = '#dbdbdb' 
COLOR_FRAMEBG_OK = '#7ede73'
INIT_PATH_ARCHIVE_ZIP = Utility.GetKeyValueinConfig("INIT_PATH_ARCHIVE_ZIP", "InitPath") 
INIT_PATH_PE_SRC= Utility.GetKeyValueinConfig("INIT_PATH_PE", "InitPath") 
INSTALL_TEMP_PATH = Utility.GetKeyValueinConfig("INSTALL_TEMP_PATH", "InitPath") 
UPDATE_TEMP_PATH = Utility.GetKeyValueinConfig("UPDATE_TEMP_PATH", "InitPath") 
PATH_PEINARCHIVE = Utility.GetKeyValueinConfig("PATH_PEINARCHIVE", "InitPath") 


# function def
def main():
    if os.path.isfile(Utility.PATH_CONFIG):
        Utility.utDeleLog()
        Utility.Dbg_print("Builder Start")
        mainWindow.mainloop() 
    else:
        Utility.Dbg_print("Find no config.ini") 

def del_bin():
    if os.path.isdir("archive"):
        shutil.rmtree(os.getcwd() + "/archive")

def buildISO():
    InsDIR = INSTALL_TEMP_PATH + ent_version.get()
    UpdDIR = UPDATE_TEMP_PATH + ent_version.get()


    # Build Install CD
    Utility.DeleteTargetFileinConfig("DeleteFile_Install")
    Utility.utMkdir(INSTALL_TEMP_PATH)
    #shutil.make_archive(name, format, archive_from, archive_to)
    shutil.make_archive(INSTALL_TEMP_PATH + "/archive", 'zip', "archive", "bin")  #zip
    Utility.Dbg_print('Make Install version to: '+ INSTALL_TEMP_PATH + "/archive")
    Utility.utCheckFilesinFolder("INSTALL")
    Utility.utBuildFolderToISO(INSTALL_TEMP_PATH, InsDIR)


    # Then Build Update CD, and it will also exclude the file in [DeleteFile_Install] 
    Utility.DeleteTargetFileinConfig("DeleteFile_Update")
    Utility.utMkdir(UPDATE_TEMP_PATH)
    shutil.make_archive(UPDATE_TEMP_PATH + "/Win10/archive", 'zip', "archive", "bin")
    Utility.Dbg_print('Make Update version to: '+ UPDATE_TEMP_PATH + "/Win10/archive")
    Utility.utCheckFilesinFolder("UPDATE")
    Utility.utBuildFolderToISO(UPDATE_TEMP_PATH, UpdDIR)
    
    frame_step3["bg"] = COLOR_FRAMEBG_OK

    #if detele temp folder checkbox

    return

    
def openfile():
    try:
        # Get archive.zip and unzip 
        # path_archive0 = filedialog.askopenfilename(parent=mainWindow, initialdir = INIT_PATH_ARCHIVE_ZIP,
        # filetypes = (("zip files","*.zip"),("all files","*.*")))
        with open(filedialog.askopenfilename(parent=mainWindow, initialdir = INIT_PATH_ARCHIVE_ZIP,
        filetypes = (("zip files","*.zip"),("all files","*.*"))), encoding='utf-8') as path_archive:
            if path_archive == "":
                Utility.Dbg_print('User select nothing')
                return
            else:
                Utility.Dbg_print('Select: ' + path_archive.name)

            # delete bin
            if os.path.isdir("bin"):
                shutil.rmtree(os.getcwd() + "/bin")

            zip_func.fileunzip(path_archive.name)

        # Set version number in ApplicationInfoConfig.xml
        Utility.Dbg_print('Set Version...')
        path_versionxml = os.getcwd() + Utility.GetKeyValueinConfig("VERSION_XML", "InitPath")
        if not os.path.isfile(path_versionxml):
            Utility.Dbg_print("Find no ApplicationInfoConfig.xml, please check the archive.")
            return
            
        with open(path_versionxml, "r", encoding='utf-8') as fpxml:
            list_xml = fpxml.readlines()
            for line in list_xml:        
                if line.find("Name=\"ApplicationVersion\"") != -1:
                    ori_version = Utility.GetValueFromAttributeName(line, "Value")
                    line = line.replace(ori_version, ent_version.get())
                    list_xml[6] = line
    
    
        with open(path_versionxml, "w", encoding='utf-8') as fpxml:
            for line in list_xml:
                fpxml.write(line)
        # fpxml.close

        # PE
        Utility.Dbg_print("Copy PE...")
        if os.path.isdir(PATH_PEINARCHIVE):
            shutil.rmtree(os.getcwd() + "/" + PATH_PEINARCHIVE)
        else:
            Utility.Dbg_print("Path not exsit: PATH_PEINARCHIVE")
            return
        #copy PE in
        if os.path.isdir(INIT_PATH_PE_SRC):
            shutil.copytree(INIT_PATH_PE_SRC,PATH_PEINARCHIVE)
        else:
            Utility.Dbg_print("Path not exsit: INIT_PATH_PE_SRC")      
            return  

        # Delete Files in PE (reserved)
        Utility.DeleteTargetFileinConfig("DeleteFile_PE")

        btn_buildVer["state"] = "normal"
        frame_step2["bg"] = COLOR_FRAMEBG_OK
        Utility.Dbg_print("Set version number ok.")
        return
    except Exception as e:
        Utility.Dbg_print("openfile(): " + str(e))


PADIN = 5
PADOUT = 10

mainWindow = tk.Tk()
mainWindow.title("Win10 Version Builder   (" + __file__ + ")")
mainWindow.geometry('700x250')
mainWindow.resizable(False, False)

# Frame 1 
frame_step1 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_OK)
frame_step1.grid(column=0, row=0)

label_step1 = tk.Label(frame_step1, text="Step 1. Enter Version Number", font=('Arial', 14))
label_step1.grid(column=0, row=0, ipadx = PADIN, ipady = PADIN, padx=PADOUT, pady=PADOUT)

ent_version = tk.Entry(frame_step1, width=24, font=('Arial', 14))
ent_version.grid(column=1, row=0, ipadx = PADIN+5, ipady = PADIN, padx=PADOUT, pady=PADOUT)
now = datetime.now()
str_date = now.strftime("%Y%m%d")
ent_version.insert(0, "1.300.6432_"+str_date)

# Frame 2 
frame_step2 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_UNDO)
frame_step2.grid(column=0, row=1)

label_step2 = tk.Label(frame_step2, text="Step 2. Select archive and Set version number ", font=('Arial', 14))
label_step2.grid(column=0, row=0, ipadx = PADIN, ipady = PADIN, padx=PADOUT, pady=PADOUT)

btn1 = tk.Button(frame_step2, text="Select archive", bg='white', font=('Arial', 14), command=openfile)
btn1.grid(column=1, row=0, ipadx = PADIN, ipady = PADIN, padx=PADOUT, pady=PADOUT)    

# Frame 3
frame_step3 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_UNDO)
frame_step3.grid(column=0, row=2)

label_step3 = tk.Label(frame_step3, text="Step 3. Build Install and Update ISO CD            ", font=('Arial', 14))
label_step3.grid(column=0, row=0, ipadx = PADIN+2, ipady = PADIN, padx=PADOUT, pady=PADOUT)

btn_buildVer = tk.Button(frame_step3, text="Build Version", bg='white', font=('Arial', 14), command=buildISO)
btn_buildVer.grid(column=1, row=0, ipadx = PADIN, ipady = PADIN, padx=PADOUT, pady=PADOUT)    
#btn_buildVer["state"] = "disabled"

btn_delbin = tk.Button(mainWindow, text="Del Bin", bg='white', font=('Arial', 14), command=del_bin)
btn_delbin.grid(column=1, row=0, padx=10)

if __name__ == '__main__':
    main() 

