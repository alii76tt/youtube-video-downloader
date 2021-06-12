from django.shortcuts import render, redirect
from django.http import FileResponse

#To download YouTube Videos
from pytube import YouTube
#To download YouTube content and get metadata
import pafy


# Create your views here.

def youtube_download(request):
    
    if request.method=="POST":   
        url=request.POST.get('link')
        youtube_video=pafy.new(url)
        embededlink=url.replace("watch?v=","embed/")
        context={
            'embedlink':embededlink,

            'video':youtube_video,
            'title' : youtube_video.title,
            'author' : youtube_video.author,
            'duration' : youtube_video.duration,
        }
        return render(request,'home.html',context)
    return render(request,'home.html')
