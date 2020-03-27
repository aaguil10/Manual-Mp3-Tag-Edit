#!/bin/env python
import eyed3
import urllib
import shutil
import os
import re
from os import listdir
from os.path import isfile, join


def moveToFinishedFolder(mp3_path, new_name):
    shutil.copyfile(mp3_path, 'finished/' + new_name)
    os.remove(mp3_path)


def createFileName(name, artist):
    artist = artist.replace(' ', '_').replace('\'', '')
    name = name.replace(' ', '_').replace('\'', '')
    name = re.sub('[^A-Za-z0-9_]+', '', name)
    artist = re.sub('[^A-Za-z0-9_]+', '', artist)
    filename = artist + '_' + name + ".mp3"
    return filename


def addAlbumArt(audiofile):
    albumart_url = input("Enter album art url: ")
    type(albumart_url)

    if albumart_url == "":
        return

    albumart_url = "album_art/" + albumart_url
    try:
        imagedata = None
        try:
            response = urllib2.urlopen(albumart_url)
            imagedata = response.read()
        except:
            imagedata = open(albumart_url, 'rb').read()

        audiofile.tag.images.set(
            3, imagedata, "image/jpeg", u"you can put a description here")
        audiofile.tag.save()
    except:
        print('Unable to add album art for ' + albumart_url)
        addAlbumArt(audiofile)


def fixMp3Data(mp3_path, track_data):
    audiofile = eyed3.load(mp3_path)
    audiofile.tag.title = track_data[u'name']
    audiofile.tag.artist = track_data[u'artist']
    audiofile.tag.album = track_data[u'album']
    addAlbumArt(audiofile, track_data[u'album_img_url'])
    audiofile.tag.save()

def printMp3Data(audiofile):
    title = audiofile.tag.title
    if title != None : print("title: " + audiofile.tag.title)

    artist = audiofile.tag.artist
    if artist != None : print("artist: " + audiofile.tag.artist)

    album = audiofile.tag.album
    if album != None : print("album: " + audiofile.tag.album)


def dataEntryLoop(audiofile):
    title = input("Enter new title: ")
    type(title)

    artist = input("Enter new artist: ")
    type(artist)

    album = input("Enter new album: ")
    type(album)

    print("--------")
    print("title: " + title)
    print("artist: " + artist)
    print("album: " + album)
    print("--------")

    anwser = input("Is this correct?(y/n) ")
    type(anwser)

    if anwser == "y":
        try:
#            audiofile.tag.title = str(title, "utf-8")
#            audiofile.tag.artist = str(artist, "utf-8")
#            audiofile.tag.album = str(album, "utf-8")
            audiofile.tag.title = title
            audiofile.tag.artist = artist
            audiofile.tag.album = album
            audiofile.tag.save()
        except Exception as e:
            print("Error: " + str(e))
            dataEntryLoop(audiofile)


    if anwser == "n":
        dataEntryLoop(audiofile)



mypath = 'manual_edit'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print("Total files: " + str(len(onlyfiles)))
count = 1
for file_item in onlyfiles:
    if "DS_Store" in file_item:
        continue
    try:
        status = str(count) + " of " + str(len(onlyfiles))
        print("****** " + status + " *******")
        print(file_item)
        print("*********************")
        count = count + 1
        file_path = mypath + "/" + file_item
        audiofile = eyed3.load(file_path)

        printMp3Data(audiofile)

        dataEntryLoop(audiofile)

        addAlbumArt(audiofile)




    except Exception as e:
        print(str(e))
        print("Something went wrong with: " + file_item)







