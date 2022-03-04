from django.shortcuts import render, redirect
from django.http import FileResponse

#To download YouTube Videos
from pytube import YouTube
#To download YouTube content and get metadata
import pafy
# remove self._dislikes = self._ydl_info['dislike_count'] KeyError: 'dislike_count'
#Youtube does no longer have a dislike count, they simply removed it.


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
