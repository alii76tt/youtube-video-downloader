from django.shortcuts import render
from .forms import DownloadForm
# package
import youtube_dl as yt
# check video url
import re


def index(request):
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        url = form.cleaned_data.get("url")
        # check video url
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        if not re.match(regex, url):
            context = {
                'error': "Please enter correct url!",
                'form': form
            }
            return render(request, 'home.html', context)

        yt_opts = {}

        with yt.YoutubeDL(yt_opts) as ydl:
            try:
                meta = ydl.extract_info(
                    url, download=False)
                video = True
            except:
                context = {
                    'error': "Video unavailable. Please enter correct url!",
                    'form': form
                }
                return render(request, 'home.html', context)

        video_audio_streams = []
        audioStreams = []
        for item in meta['formats']:
            file_size = item['filesize']
            itemFormat = item['format_note']

            resolution = 'Audio'
            if item['height'] is not None:
                resolution = f"{item['height']}x{item['width']}"

            if 'Audio' in resolution:
                audioStreams.append({
                    'resolution': resolution,
                    'extension': item['ext'],
                    'file_size': file_size,
                    'itemFormat': itemFormat,
                    'url': item['url'],
                })
            else:
                video_audio_streams.append({
                    'resolution': resolution,
                    'extension': item['ext'],
                    'file_size': file_size,
                    'itemFormat': itemFormat,
                    'url': item['url']
                })
        video_audio_streams = video_audio_streams[::-1]

        context = {
            'form': form,
            'isVideo': video,
            'url': url,
            'title': meta['title'],
            'streams': video_audio_streams,
            'audioStreams': audioStreams,
            'channel': meta['channel'],
            'likes': meta['like_count'],
            'image': meta['thumbnails'][3]['url'],
            'duration': round(int(meta['duration'])/60, 2),
            'views': f'{int(meta["view_count"]):,}'
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html', {'form': form})
