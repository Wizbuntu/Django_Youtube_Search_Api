from django.shortcuts import render
from django.http import HttpResponse
import requests

from isodate import parse_duration
from django.conf.urls.static import settings

from datetime import datetime
from dateutil import relativedelta
from dateutil import parser

from math import floor, log

from .models import Youtube_Search_Api
from django.http import JsonResponse


# Create your views here.


def index(request):
    return render(request, 'youtube_api/index.html', {})

def home(request):
    if request.method == "GET":
        videos = []
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
                'part' : 'snippet',
                'q' : request.GET.get('search'),
                'key' : settings.YOUTUBE_API_KEY,
                'maxResults' : 50,
                'type' : 'video'
            }

        r = requests.get(search_url, params=search_params)

        results_search = r.json()['items']

        # print(results_search)
        video_ids = []
        for result in results_search:
            video_ids.append(result['id']['videoId'])

        video_params = {
                'key' : settings.YOUTUBE_API_KEY,
                'part' : 'snippet,contentDetails,statistics',
                'id' : ','.join(video_ids),
                'maxResults' : 50
            }

        r = requests.get(video_url, params=video_params)

        results_video = r.json()['items']
     
        for result in results_video:
                # Convert view Count to abbreviated String
                units = ['', 'K', 'M', 'B', 'T', 'P']
                k = 1000.0
                magnitude = int(floor(log(int(result['statistics']['viewCount']), k)))
                view_count = '%.1f%s' % (int(result['statistics']['viewCount']) / k**magnitude, units[magnitude])
                
            

                # calculate datetime difference
                date_time1 = datetime.now()
                date_time2 = parser.parse(result['snippet']['publishedAt'], ignoretz=True) 
                diff = relativedelta.relativedelta(date_time1, date_time2)
                # print('{} years ago'.format(diff.years))
                # print(date_time1, date_time2)

                video_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                    'createdAt': result['snippet']['publishedAt'],
                    'date': '{} years {} months ago'.format(diff.years, diff.months),
                    'viewCount': result['statistics']['viewCount'],
                    'view_count': view_count
                }

                
                

                videos.append(video_data)


        return JsonResponse(videos, safe=False)

    else:
        return render(request, 'youtube_api/index.html', {})



    


    