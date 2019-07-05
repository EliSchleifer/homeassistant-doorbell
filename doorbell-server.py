"""Doorbell Server

To use the script:

 * Drop this script into a folder that, besides python files, contains
nothing but music files

doorbell-server.py 

"""

from __future__ import print_function, unicode_literals

import errno
import os
import os.path
import random
import sys
import socket
import time
import threading

from threading import Thread
from random import choice
from collections import namedtuple

from urllib.parse import quote, urlsplit, parse_qs
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import TCPServer, ThreadingMixIn

from mutagen.mp3 import MP3

music_files = []

playing_until = time.time()

AudioFile = namedtuple("AudioFile", "url length name key")

def is_doorbell_busy():
    global playing_until
    return time.time() < playing_until


 
class CustomRequestHandler(SimpleHTTPRequestHandler):   

    def send_redirect(self, location):
        self.send_response(301)
        self.send_header('Location', location)
        self.end_headers()

    def send_text_response(self, code, body):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        bytes = "<body>{} - {}</body>".format(code, body).encode('utf-8')
        self.wfile.write(bytes)
       
    def do_GET(self):
        global playing_until
        if self.path.startswith('/doorbell_press'):    
            if is_doorbell_busy():
                self.send_text_response(429, "Doorbell already playing")
                return
                
            query = urlsplit(self.path).query            
            params = parse_qs(query)
            
            file_to_play = None
            requested_ringtone = "ringtone" in params and params["ringtone"]
            if requested_ringtone:                
                for file in music_files:                 
                    key = ''.join(params["ringtone"][0].split())                
                    if file.key == key:
                        file_to_play = file
                
            if not file_to_play:
                if requested_ringtone:
                    # A ringtone was requested but not found
                    msg = "Ringtone not found<br/><ul>"
                    for file in music_files:
                        msg += "<li>" + file.name + "</li>"
                    msg += "</ul>"
                    self.send_text_response(404, msg)
                    return
                else:
                    # Pick random ringtone
                    file_to_play = random.choice(music_files)                                

            msg = "Doorbell received (request_id:{})".format(random.randint(1, 1000))                            
            print(msg)
            http_path = self.server.root_path + "/" + file_to_play.url
            print('on_doorbell {} '.format(file_to_play.name))
            # Update playing until end of the song
            playing_until = time.time() + file_to_play.length
            self.send_redirect(http_path)
        else:
            try:
                super().do_GET()      
            except BrokenPipeError:
                pass

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def get_server(port, retry_bind, serve_path=None):
    Handler = CustomRequestHandler
    if serve_path:
        Handler.serve_path = serve_path
    while retry_bind >= 0:
        try:
            httpd = ThreadingHTTPServer(("", port), Handler)
            return httpd
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                retry_bind -= 1
                time.sleep(3)
                print("Waiting 3 seconds for port to open...")
            else:
                raise   
    
def load_music_files():
    """Add all music files from this folder and subfolders"""
    # Make a list of music files, right now it is done by collection all files
    # below the current folder whose extension starts with mp3/wav    
    print('Loading music files...')
    for path, dirs, files in os.walk('.'):
        for file_ in files:
            file_path = os.path.relpath(os.path.join(path, file_))
            url_path = os.path.join(*[quote(part) for part in os.path.split(file_path)])                
            ext = os.path.splitext(file_)[1].lower()
            name = os.path.splitext(file_)[0].lower()
            key = ''.join(name.split()) # unique key - no spaces
            audio_file = None
            if ext.startswith('.mp3'):
                audio = MP3(file_path)                                
                audio_file = AudioFile(url_path, audio.info.length, name, key)            
            if audio_file:
                music_files.append(audio_file)
                print('Found:', music_files[-1])

def detect_ip_address():
    """Return the local ip-address"""
    # Rather hackish way to get the local ip-address, recipy from
    # https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def parse_args():
    """Parse the command line arguments"""
    import argparse
    description = 'Return local mp3 files'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--port', default=8888, type=int,
                        help='The local machine port to run the webser on')
    parser.add_argument('--ip', default=None, type=str,
                        help='The local IP address of this machine. By '
                        'default it will attempt to autodetect it.')
    parser.add_argument('--file_root', default='',
                        help='The folder in this machine to serve as the root for '
                        'the audio files. Default is current working directory')

    return parser.parse_args()

def main():
    # Settings
    args = parse_args()

    if not args.ip:
        args.ip = detect_ip_address()

    print(" Will use the following settings:\n"
          " IP to use: {args.ip}\n"
          " Use port: {args.port}\n"
          " File root: {args.file_root}".format(args=args))          
        
    try:
        if args.file_root:
            print("File root: {0}".format(args.file_root))
            os.chdir(args.file_root)
        else:
            print("File root: {}".format(os.getcwd()))
        load_music_files()
        http_server = get_server(args.port, 100, None)
        http_server.root_path = "http://{}:{}".format(args.ip, args.port)
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")
        http_server.server_close()
        http_server.socket.close()

main()
