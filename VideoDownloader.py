import math
import os
import sys
import shutil
from pytube import YouTube,Playlist,Stream

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def on_complete(stream,fileLocation):
    print("Download")

def fileSize(url): # <-- For file size checking
    filesize = YouTube(url).streams.get_by_itag(22).filesize 
    return filesize
def on_progress(
    stream: Stream, chunk: bytes, bytes_remaining: int):
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)

def display_progress_bar(bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55):
    """Display a simple, pretty progress bar.

    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%

    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param str ch:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multiplier to reduce progress bar size.

    """
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = f" ↳ |{progress_bar}| {percent}%\r"
    sys.stdout.write(text)
    sys.stdout.flush()


def Video(url,fileLocation,want_download=False):
    '''Helps rename video files in a way and you want to download give True if no playlist link,Video Download'''
    try:
        if "playlist" in url:
            playlist = Playlist(url)
            os.chdir(fileLocation)
            # 22 for 720 p
            fqual=22
            # Below give File Formate
            fileFormate='.mp4'
            counter = 0
            not_download=[]
            ''' Iam Store The Download Pending names '''
            print("I am In Working Please Wait .... ")
            for video_name in os.walk(os.getcwd()):
                print(f'Downloading: {playlist.title} playlist')  
                for video,lin in zip(playlist.videos,playlist):
                    # Below here change the videoTitle with existing one reference
                    videoTitle=video.title.replace('|', ' ').replace('/',' ').replace('('," ").replace(')'," ").replace(',',' ')                            
                    counter += 1
                    vName=f'{videoTitle}{fileFormate}'
                    EvideoTitle=f"{counter} - {vName}"
                    filesize=fileSize(lin)
                    if EvideoTitle in video_name[2]:
                        if want_download and os.path.getsize(f"{fileLocation}\\{EvideoTitle}") != filesize:
                            print(f'Downloading ... 720p ...{video.title} and filesize({convert_size(filesize)})')
                            video=YouTube(lin,on_progress_callback=on_progress,on_complete_callback=on_complete)
                            video.streams.get_by_itag(fqual).download(filename=f'{counter} - {videoTitle}', output_path=f'{fileLocation}')
                            print(f'Download Completed:- {video.title}')
                        else:
                            print(f'Its Downloaded/Renamed:- Video {counter} - {vName}')
                    elif vName in video_name[2]:
                        os.rename(vName,f"{counter} - {vName}")
                        print(f"Video: Renamed-To : {counter} - {vName}")
                    elif want_download:
                        print(f'Downloading ... 720p ...{video.title} and filesize({convert_size(filesize)} Bytes)')
                        video=YouTube(lin,on_progress,on_complete)
                        video.streams.get_by_itag(fqual).download(filename=f'{counter} - {videoTitle}', output_path=f'{fileLocation}')
                        print(f'Download Completed:- {video.title}')
                    else:
                        not_download.append(f"Video: {counter} - {videoTitle}")
                        # print(f"Video: {counter} - {video.title} Not Downloaded Yet / Check Out The Name.")
            for pending_download in not_download:
                print(f"Pending Downloades : {pending_download}")
        else:
            video=YouTube(url)
            videoTitle=video.title.replace('|', ' ').replace('/',' ').replace('('," ").replace(')'," ").replace(',',' ')
            fileSize1 = YouTube(url).streams.get_by_itag(22).filesize
            if os.path.getsize(f"{fileLocation}\\{videoTitle}{fileFormate}") != fileSize1:
                video=YouTube(url,on_progress_callback=on_progress,on_complete_callback=on_complete)
                print("Download Starting ... 720p",convert_size(fileSize1))
                video.streams.get_by_itag(fqual).download(filename=vName,output_path=fileLocation)
                os.rename(video.streams.first().default_filename,f"{video.title.replace('|','').replace('/','').replace('(',' ').replace(')',' ').replace(',',' ')}{fileFormate}")
                print(f'Download Completed at {fileLocation}')
            else:
                print("Its downloaded Already")
    except Exception as e:
        print("Check The Internet Connection And Also See The Error Name:",e,"\nError at MakeOrder function")
    finally:
        print("")
        print("My Job Done!")   
