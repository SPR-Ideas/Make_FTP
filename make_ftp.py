#!/usr/bin/python3
"""
    Title : Instant FTP.

    Description:
        This is script created for generating Instant
        Http File server using ngrok tool.
"""
from threading import Thread
import sys
import os
import time
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from pyngrok import ngrok

ftp_file = FastAPI()

FILE_PATH = ""
KILL = "kill -9 "
RUN_TIME = 60*10  # mention total run time in seconds
START_ = bool()
CREATED_ZIP_FILE = False

@ftp_file.get("/")
def give_file():
    """
        The function is used to give a file response
        when anyone send request to the ngrok link
    """
    file_name = FILE_PATH.split("/")
    file_name = file_name[-1]
    return FileResponse(
                path = FILE_PATH ,
                filename=file_name ,
                media_type="text/all")


def stop_after_awhile(pid,start_time):
    """
        IT runs on an another Thread,
        inordered to Kill the server after the specified
        RUN_TIME.
    """
    ngrok_obj = ngrok.connect(8000,"http")
    print("\n\t{} -> {}\n".format(FILE_PATH,ngrok_obj.public_url))
    print("\n Press (Ctrl + C ) for closing the server")
    while time.time() - start_time <= RUN_TIME and START_:
        pass

    if CREATED_ZIP_FILE:
        os.remove(FILE_PATH)

    ngrok.disconnect(ngrok_obj.public_url)
    os.system(KILL+str(pid))


def start_servering_file():
    """
        Starts To server the File, which is the
        mentioned in FILE_PATH
    """
    global START_
    stop_call_thread = Thread(
            target=stop_after_awhile,
            args=(
                os.getpid(),
                time.time()
            ))
    stop_call_thread.start()

    uvicorn.run(ftp_file,host="0.0.0.0",port=8000)
    START_ = False


def update_file_location(file_name):
    """
        Update the current File location on FILE_PATH
    """
    global FILE_PATH

    path_object = Path(file_name)
    FILE_PATH = path_object.absolute().as_posix()

    if os.path.isdir(FILE_PATH):
        FILE_PATH += "/"
        make_zip_file_and_update_path()

    if os.path.exists(FILE_PATH):
        return True

    print("File does not exist.")
    return False


def make_zip_file_and_update_path():
    """
        Make zip_file of the current Folder.
    """
    global CREATED_ZIP_FILE
    global FILE_PATH

    CREATED_ZIP_FILE = True

    temp=FILE_PATH.replace(".","")+FILE_PATH.split('/')[-2]
    os.system("zip {}.zip -r .".format(temp))
    FILE_PATH = temp+".zip"


def generate_link():
    """
        It generates link to server a project in compressed format.
    """
    if update_file_location(sys.argv[1]):
        start_servering_file()


def help_():
    msg = """
        make_ftp <usage> :
            usage:
            file_path : file_location can be absolute or relative
                        relative path.
    """
    print(msg)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        START_ = True
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            help_()
        else:
            generate_link()
    help_()