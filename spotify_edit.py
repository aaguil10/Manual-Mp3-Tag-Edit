
import eyed3
import urllib.request
import shutil
import os
import re
from os import listdir
from os.path import isfile, join
import spotipy
import spotipy.util as util
import os

username = os.environ['SPOTIPY_USERNAME']

def getSpotipy():
    scope = 'user-library-read,playlist-modify-private,playlist-modify-public,user-read-recently-played, user-library-modify'
    token = util.prompt_for_user_token(username, scope)
    if token:
        return spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
        return null

def moveToFinishedFolder(mp3_path, new_name):
    shutil.copyfile(mp3_path, mypath + '/' + new_name)
    os.remove(mp3_path)


def createFileName(name, artist):
    artist = artist.replace(' ', '_').replace('\'', '')
    name = name.replace(' ', '_').replace('\'', '')
#    name = re.sub('[^A-Za-z0-9_]+', '', name)
#    artist = re.sub('[^A-Za-z0-9_]+', '', artist)
    filename = artist + '_' + name + ".mp3"
    return filename


def enterAlbumArtManually(audiofile):
    albumart_url = input("Enter album art url: ")
    type(albumart_url)

    if albumart_url == "":
        return

    try:
        imagedata = None
        try:
            response = urllib.request.urlopen(albumart_url)
            imagedata = response.read()
        except Exception as e:
            print(albumart_url + " not url")
            print(str(e))
            albumart_url = "album_art/" + albumart_url
            imagedata = open(albumart_url, 'rb').read()

        audiofile.tag.images.set(
            3, imagedata, "image/jpeg", u"you can put a description here")
        audiofile.tag.save()
    except Exception as e:
        print('Unable to add album art for ' + albumart_url)
        print(str(e))
        enterAlbumArtManually(audiofile)


def addSpAlbumArt(audiofile, albumart_url):
    try:
        imagedata = None
        try:
            response = urllib.request.urlopen(albumart_url)
            imagedata = response.read()
        except Exception as e:
            print(albumart_url + " not url")
            print(str(e))
            enterAlbumArtManually(audiofile)

        audiofile.tag.images.set(
            3, imagedata, "image/jpeg", u"you can put a description here")
        audiofile.tag.save()
    except Exception as e:
        print('Unable to add album art for ' + albumart_url)
        print(str(e))
        addAlbumArt(audiofile)

def printMp3Data(audiofile):
    title = audiofile.tag.title
    if title != None : print("title: " + audiofile.tag.title)

    artist = audiofile.tag.artist
    if artist != None : print("artist: " + audiofile.tag.artist)

    album = audiofile.tag.album
    if album != None : print("album: " + audiofile.tag.album)


def spotify_loop(audiofile):
    uri = input("Enter spotify URI: ")
    type(uri)
    
    sp = getSpotipy()
    track = sp.track(uri)
    title = track['name']
    artist = track['artists'][0]['name']
    album = track['album']['name']
    
    print("--------")
    print("title: " + title)
    print("artist: " + artist)
    print("album: " + album)
    print("--------")
    
    anwser = input("Is this correct?(y/n) ")
    type(anwser)

    if anwser == "y":
        try:
            audiofile.tag.title = title
            audiofile.tag.artist = artist
            audiofile.tag.album = album
            audiofile.tag.save()
            addSpAlbumArt(audiofile, track['album']['images'][0]['url'])
        except Exception as e:
            print("Error: " + str(e))
    if anwser == "n":
        spotify_loop(audiofile)


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

        spotify_loop(audiofile)
        
        new_name = createFileName(audiofile.tag.title, audiofile.tag.artist)
        moveToFinishedFolder(file_path, new_name)

    except Exception as e:
        print(str(e))
        print("Something went wrong with: " + file_item)







