import os.path
import tempfile
import subprocess
import requests
import re

class AudioProc:

    __regex = "https.*key.pub"
    __regex_2 = '"https.*pub?.*"'
    __regex_3 = 'ts?.*'

    def parse_m3u8(self,url):
        urldir = os.path.dirname(url)
        playlist = requests.get(url).text
        keyurl = re.findall(self.__regex, playlist)[0]
        key = requests.get(keyurl).text

        for match in re.finditer(self.__regex_2, playlist, re.MULTILINE):
            playlist = playlist.replace(match.group(), 'key.pub')

        for match in re.finditer(self.__regex_3, playlist):
            playlist = playlist.replace(match.group(), 'ts')

        return playlist, key, urldir

    def download_m3u8(self,playlist, key, urldir, output='out.mp3'):
        ts_list = [x for x in playlist.split('\n') if not x.startswith('#')]

        with tempfile.TemporaryDirectory(output) as dir_:

            for file in ts_list[:-1]:
                with open(dir_+"/"+file, 'wb') as audio:
                    audio.write(requests.get(os.path.join(urldir, file)).content)
            with open(dir_+"/"+'key.pub', 'w') as keyfile:
                keyfile.write(key)
            with open(dir_+"/"+'index.m3u8', 'w') as playlist_file:
                playlist_file.write(playlist)

            subprocess.call(['ffmpeg', '-allowed_extensions', "ALL", '-protocol_whitelist',
                             "crypto,file", '-i', dir_+"/"+'index.m3u8', '-c', 'copy', f'{dir_+"/"+output}'])

            return open(dir_+"/"+output, 'rb').read()