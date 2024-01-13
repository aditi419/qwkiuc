import socket
from threading import Thread
import ftplib
from ftplib import FTPHandler
import os
import time
import ntpath
from pathlib import Path 

IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()

setup()

def musicWindow():
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog

    window = Tk()
    window.title("Music Window")
    window.geometry("300x300")
    window.configure(bg="LightSkyBlue")

    selectLabel = Label(window, text="Select Song", bg="LightSkyBlue", font = ("Calibri",8))
    selectLabel.place(x=2,y=1)

    listbox = Listbox(window, height=10, width=39, activestyle="dotbox", bg="LightSkyBlue", borderwidth=2, font = ("Calibri",8))
    listbox.place(x=10,y=10)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1, relx=1)
    scrollbar1.config(command=listbox.yview)

    PlayBtn = Button(window, text="Play", width=10, bd=1, bg="SkyBlue", font = ("Calibri",8))
    PlayBtn.place(x=30,y=200)

    Stop = Button(window, text="Stop", bd=1, width=10, bg="SkyBlue", font = ("Calibri",8))
    Stop.place(x=200,y=200)

    Upload = Button(window, text="Upload", width=10, bd=1, bg="SkyBlue", font = ("Calibri",8))
    Upload.place(x=30,y=250)

    Download = Button(window, text="Download", width=10, bd=1, bg="SkyBlue", font = ("Calibri",8))
    Download.place(x=200,y=250)

    infoLabel = Label(window, text="", fg="blue", font = ("Calibri",8))
    infoLabel.place(x=4,y=280)

    window.mainloop()

def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp.cwd('shared_files')
        fname = ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR (fname)", file)

        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter, fname)
        song_counter = song_counter + 1

    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    song_to_download = listbox.get(ANCHOR)
    infoLabel.configure(text="Downloading " + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary("RETR " + song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text="Download Complete")
    time.sleep(1)
    if(song_selected != ""):
        infoLabel.configure(text="Now Playing" + song_selected)
    else:
        infoLabel.configure(text="")