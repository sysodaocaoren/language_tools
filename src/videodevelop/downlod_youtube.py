import pytube
from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")

#
# link = input("https://www.youtube.com/watch?v=W-po628uyUE")
# Download(link)

# YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download() https://www.youtube.com/watch?v=W4QmDg517tk
yt = YouTube('https://youtube.com/watch?v=Rgz2xzfXslI ')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()