import urllib.request
import os
import magic
import cv2
import socket
from time import sleep      
import threading as td

true = True


def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False


def json_response():
    try:
        url = "http://192.168.204.57:9012/download"
        response = urllib.request.urlopen(url)
        data = response.read()
        dat = eval(data.decode('ascii'))
        return dat
    except Exception as e:
        print(e)
        return False


l_duration = []
active_asset = []
asset=[]

def downloading():
    global asset
    global active_asset
    global l_duration
    active_asset=[]
    asset=[]
    l_duration=[]
    try:
        if internet():
            data = json_response()
            asset = data['asset']
        path = "/home/pi/innosignage/media"
        os.chdir(path)
        for obj in asset:
            assetid = obj['id']
            url1 = "http://192.168.204.57:9012/fetching_asset/" + str(assetid)
            name = obj['name']
            active_asset.append(name)
            duration = obj['duration']
            t = (name, duration)
            l_duration.append(t)
            urllib.request.urlretrieve(url1, name)
            sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

def delete_other():
    global active_asset
    try:
        path = "/home/pi/innosignage/media"
        os.chdir(path)
        current_files = os.listdir()
        print("current:",current_files)
        print(active_asset)
        for i in current_files:
            if i not in active_asset:
                os.system('rm -r ' + i)
        return True
    except:
        print("deletion error")
        return False

fixedfiles = ['welcome.png', 'noconnection.png']


def Assetplay():
    path = "/home/pi/innosignage/media"
    os.chdir(path)
    if os.listdir():
        name = os.listdir()
        for image in name:
            if 'image' in magic.from_file(image):  # to check type of file 'I'/'V'
                subprocess.Popen("feh -q -p -Z -F -R 60 -Y "+image,shell=True)
                sleep(15)
            else:
                subprocess.Popen('omxplayer ' + image,shell=True)
        if internet():
            displayer()
        else:
            Assetplay()
    else:
        path = "/home/pi/innosignage/default"
        os.chdir(path)
        for i in fixedfiles:
            subprocess.Popen("feh -q -p -Z -F -R 60 -Y "+image[0],shell=True)
            sleep(15)
        if internet():
            displayers()
        else:
            Assetplay()

import subprocess

def displayer():
    path = "/home/pi/innosignage/media"
    os.chdir(path)
    global asset
    global l_duration
    while True:
        try:
            if internet():
                json_data = json_response()
                json_data = json_data['asset']
                if json_data == asset:
                    if os.listdir():
                        pass
                    else:
                        Assetplay()
                    for image in l_duration:
                        if 'image' in magic.from_file(image[0]):  # to check type of file 'I'/'V'
                            subprocess.Popen("feh -q -p -Z -F -R 60 -Y "+image[0],shell=True)
                            sleep(image[1])
                        else:
                            subprocess.Popen('omxplayer ' + image[0])
                else:
                    downloading()
                    delete_other()
            else:
                Assetplay()
        except Exception as e:
            print(e)
            print("format Not supported")
            return False
      
def main():
    path="/home/pi/innosignage"
    os.chdir(path)
    global name
    subprocess.Popen("feh -q -p -Z -F -R 60 -Y blanck.png",shell=True)
    if internet():
        t1 = td.Thread(target=downloading)
        t1.start()
        t1.join()
        displayer()
    else:
        Assetplay()

main()
