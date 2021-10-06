# Version: Python 3.9.7 64-bit
# Todo list:
# 1. Calculate SHA256 for authenticate (hard)
# 2. for other customers
# 3. UI optimize 
# 4. delete temp folder
# 
#  
# 紀錄用到的技術:
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
#       Example: "pyinstall -F ./Builder.py
#


# For GUI
import tkinter as tk 
from tkinter import filedialog

# File processing
import os
import shutil

# Others
import Utility
import zip_func


# CONST
COLOR_FRAMEBG_UNDO = '#dbdbdb' 
COLOR_FRAMEBG_OK = '#7ede73'
INIT_PATH_ARCHIVE_ZIP = Utility.GetKeyValueinConfig("INIT_PATH_ARCHIVE_ZIP", "InitPath") 
INSTALL_TEMP_PATH = Utility.GetKeyValueinConfig("INSTALL_TEMP_PATH", "InitPath") 
UPDATE_TEMP_PATH = Utility.GetKeyValueinConfig("UPDATE_TEMP_PATH", "InitPath") 


# function def
def main():
    if os.path.isfile(Utility.PATH_CONFIG):
        Utility.utDeleLog()
        Utility.Dbg_print("Builder Start")
        mainWindow.mainloop() 
    else:
        Utility.Dbg_print("Find no config.ini") 

def buildISO():
    InsDIR = INSTALL_TEMP_PATH + ent_version.get()
    UpdDIR = UPDATE_TEMP_PATH + ent_version.get()


    # Build Install CD
    Utility.DeleteTargetFileinConfig("DeleteFile_Install")
    Utility.utMkdir(INSTALL_TEMP_PATH)
    shutil.make_archive(INSTALL_TEMP_PATH + "/archive", 'zip', "../Python", "bin")  #zip
    Utility.utBuildFolderToISO(INSTALL_TEMP_PATH, InsDIR)


    # Then Build Update CD, and it will also exclude the file in [DeleteFile_Install] 
    Utility.DeleteTargetFileinConfig("DeleteFile_Update")
    Utility.utMkdir(UPDATE_TEMP_PATH)
    shutil.make_archive(UPDATE_TEMP_PATH + "/archive", 'zip', "../Python", "bin")
    Utility.utBuildFolderToISO(UPDATE_TEMP_PATH, UpdDIR)
    
    frame_step3["bg"] = COLOR_FRAMEBG_OK

    #if detele temp folder checkbox

    return

    
def openfile():
    try:
        # Get archive.zip and unzip 
        path_archive = filedialog.askopenfilename(parent=mainWindow, initialdir = INIT_PATH_ARCHIVE_ZIP,
        filetypes = (("zip files","*.zip"),("all files","*.*")))
        strent2.set(path_archive)
        if path_archive == "":
            return

        # delete bin
        if os.path.isdir("bin"):
            shutil.rmtree(os.getcwd() + "/bin")

        zip_func.fileunzip(path_archive)

        # Set version number in ApplicationInfoConfig.xml
        path_versionxml = os.getcwd() + Utility.GetKeyValueinConfig("VERSION_XML", "InitPath")
        if not os.path.isfile(path_versionxml):
            Utility.Dbg_print("Find no ApplicationInfoConfig.xml, please check the archive.")
            return
            
        fpxml = open(path_versionxml, "r")
        list_xml = fpxml.readlines()
        for line in list_xml:        
            if line.find("Name=\"ApplicationVersion\"") != -1:
                ori_version = Utility.GetValueFromAttributeName(line, "Value")
                line = line.replace(ori_version, ent_version.get())
                list_xml[6] = line
        fpxml.close        
    
        fpxml = open(path_versionxml, "w")
        for line in list_xml:
            fpxml.write(line)
        fpxml.close

        btn_buildVer["state"] = "normal"
        frame_step2["bg"] = COLOR_FRAMEBG_OK
        Utility.Dbg_print("Set version number ok.")
        return
    except Exception as e:
        Utility.Dbg_print("openfile(): Err")


mainWindow = tk.Tk()
mainWindow.title("Win10 Version Builder   (" + __file__ + ")")
mainWindow.geometry('1000x400')
mainWindow.resizable(False, False)
strent2 = tk.StringVar()

# Frame 1 
frame_step1 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_OK, width=500)
frame_step1.pack(padx=10, pady=10) 

label_step1 = tk.Label(frame_step1, text="Step 1. Enter Version Number", font=('Arial', 12))
label_step1.pack(side=tk.LEFT, padx=10, pady=10)

ent_version = tk.Entry(frame_step1, width=20, font=('Arial', 11))
ent_version.pack(side=tk.LEFT, padx=17, pady=7) 
ent_version.insert(0, "1.300.6432_20210922")

# Frame 2 
frame_step2 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_UNDO)
frame_step2.pack(padx=10, pady=10) 

label_step2 = tk.Label(frame_step2, text="Step 2. Select archive.zip and Set version number", font=('Arial', 12))
label_step2.pack(side=tk.TOP, padx=10, pady=5)

btn1 = tk.Button(frame_step2, text="Select archive", bg='white', font=('Arial', 11), command=openfile)
btn1.pack(side=tk.LEFT, padx=10, pady=5)       

ent2 = tk.Entry(frame_step2, textvariable=strent2, fg='black', width=100, font=('Arial', 11))
ent2.pack(side=tk.LEFT, padx=17, pady=7) 
ent2.insert(1, '(file path)')

# Frame 3
frame_step3 = tk.Frame(mainWindow, bg=COLOR_FRAMEBG_UNDO)
frame_step3.pack(padx=10, pady=10) 

label_step3 = tk.Label(frame_step3, text="Step 3. Build Install and Update ISO CD", font=('Arial', 12))
label_step3.pack(side=tk.TOP, padx=10, pady=5)

btn_buildVer = tk.Button(frame_step3, text="Build Version", bg='white', font=('Arial', 11), command=buildISO)
btn_buildVer.pack(side=tk.LEFT, padx=10, pady=10)  
#btn_buildVer["state"] = "disabled"
    


if __name__ == '__main__':
    main() 

