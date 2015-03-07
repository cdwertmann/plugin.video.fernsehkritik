# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import urlparse
import os
import binascii
import time
import xmltodict
from bs4 import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
PLUGIN_NAME = "plugin.video.fernsehkritik"
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# cache for one hour
cache = StorageServer.StorageServer(PLUGIN_NAME, 1)

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def log(msg):
    xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

def getLatestEp():
    return 150

#latest_ep=cache.cacheFunction(getLatestEp)
latest_ep=getLatestEp()
log(sys.argv)

def getEpDetails(ep):
    log("http://fernsehkritik.tv/folge-"+str(ep)+"/")
    response = opener.open("http://fernsehkritik.tv/folge-"+str(ep)+"/play")
    html=response.read().decode('utf-8')
    response.close()
    soup = BeautifulSoup(html)
    url = soup.find_all('source')[0]['src'] or ""
    title = soup.find('h3').contents[0] or ""
    return url, title

def addItems(start):
    if (start>latest_ep):
        start=latest_ep
    end = start-10
    if (end<0):
        end=0

    for ep in reversed(range(end+1,start+1)):
        url, title = getEpDetails(ep)
        listitem=xbmcgui.ListItem (title, iconImage='http://fernsehkritik.tv/images/magazin/folge'+str(ep)+'.jpg')
        listitem.setInfo( type="Video", infoLabels={ "title": title })
        #listitem.setProperty('IsPlayable', 'true')
        #listitem.addStreamInfo('video', {'duration': clip['duration']})
        xbmcplugin.addDirectoryItem(addon_handle, url, listitem,totalItems=start-end)

    if (end > 0):
        listitem=xbmcgui.ListItem("Weiter...", iconImage="DefaultFolder.png")
        url = build_url({'id': start-10})
        xbmcplugin.addDirectoryItem(addon_handle, url, listitem, True)


xbmcplugin.setContent(addon_handle, "episodes")


# if id=x
#     additems(x)
# else
#     additems(last_ep)

id = ''.join(args.get('id', ""))


if id!="":
    log("id"+id)
    addItems(int(id))
else:
    log("latest")
    addItems(latest_ep)

#id = ''.join(args.get('id', ""))
#content = cache.cacheFunction(getContent)
#getCategories(content, id)

# url="http://dl6.massengeschmack.tv/deliver/t/218f260fb7b0182f7b3e581247143a3f/54fa6cf4/7200/fktv/limited/fernsehkritik150.webm"
# #url = "http://dl6.massengeschmack.tv/deliver/t/9fdbbe7191dd9f7aae44ced0273da732/54fa6cf4/7200/fktv/limited/fernsehkritik150.mp4"
# items = []
# for ep in reversed(range(1,latest_ep)):
#     listitem=xbmcgui.ListItem (str(ep), iconImage='DefaultVideo.png')
#     #listitem.setInfo( type="Video", infoLabels={ "title": clip['title'], "plot": clip['description'], "aired": airdate, "date": date, "count": count})
#     #listitem.setProperty('IsPlayable', 'true')
#     #listitem.addStreamInfo('video', {'duration': clip['duration']})
#     items.append((url, listitem, False))

# xbmcplugin.addDirectoryItems(addon_handle,items)

xbmcplugin.endOfDirectory(addon_handle)
# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')



# def get_signature(key, msg):
#     return base64.b64encode(hmac.new(key, msg, hashlib.sha1).digest())

# def build_url(query):
#     return base_url + '?' + urllib.urlencode(query)

# def log(msg):
#     xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

# def getContent():
#     URL="http://cinemassacre.screenwavemedia.com/AppServer/SWMAppFeed.php?appname=Cinemassacre&appversion=1.5.8&devicetoken="+devicetoken+"&deviceuid="+deviceuid+"&lastupdateid=0&timestamp="+timestamp+"&signature="+signature
#     log(URL)
#     req = urllib2.Request(URL)
#     response = urllib2.urlopen(req)
#     xml=response.read()
#     response.close()
#     return xmltodict.parse(xml)['document']

# def getCategories(content,id):
#     items = []
#     if id=="":
#         listitem=xbmcgui.ListItem("- All videos sorted by date -", iconImage="DefaultFolder.png")
#         url = build_url({'id': "all"})
#         items.append((url, listitem, True))

#     if id=="all":
#         xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
#     else:
#         xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)

#     for cat in content['MainCategory']:
#         if cat['@parent_id'] == id:
#             #if cat['@activeInd'] == "N": continue
#             listitem=xbmcgui.ListItem(cat['@name'], iconImage="DefaultFolder.png")
#             url = build_url({'id': cat['@id']})
#             items.append((url, listitem, True))
    
#     if id!="" or id=="all":
#         count=0
#         for clip in content['item']:
#             if clip['movieURL']=="" or clip['@activeInd'] == "N": continue
#             cat_tag=clip['categories']['category']
#             cat=None
#             if type(cat_tag)==DictType:
#                 if cat_tag['@id']==id: cat=[cat_tag['@id']]
#             elif type(cat_tag)==ListType:
#                 for c in cat_tag:
#                     if c['@id']==id: cat=c['@id']

#             if not cat and id!="all": continue
#             url = clip['movieURL']
#             if not "http" in url:
#                 url = "http://video1.screenwavemedia.com/Cinemassacre/smil:"+url+".smil/playlist.m3u8"
#             elif "youtube.com" in url:
#                 url = "plugin://plugin.video.youtube/?action=play_video&videoid="+video_id(url)
#             date=None
#             airdate=None
#             if clip['pubDate']:
#                 # python bug http://stackoverflow.com/questions/2609259/converting-string-to-datetime-object-in-python
#                 d=clip['pubDate'][:-6]
#                 # python bug http://forum.xbmc.org/showthread.php?tid=112916
#                 try:
#                     d=datetime.strptime(d, '%a, %d %b %Y %H:%M:%S')
#                 except TypeError:
#                     d=datetime(*(time.strptime(d, '%a, %d %b %Y %H:%M:%S')[0:6]))

#                 date=d.strftime('%d.%m.%Y')
#                 airdate=d.strftime('%Y-%m-%d')
#             count+=1
#             listitem=xbmcgui.ListItem (clip['title'], thumbnailImage=clip['smallThumbnail'], iconImage='DefaultVideo.png')
#             listitem.setInfo( type="Video", infoLabels={ "title": clip['title'], "plot": clip['description'], "aired": airdate, "date": date, "count": count})
#             listitem.setProperty('IsPlayable', 'true')
#             listitem.addStreamInfo('video', {'duration': clip['duration']})
#             items.append((url, listitem, False))

#     xbmcplugin.addDirectoryItems(addon_handle,items)


# xbmcplugin.setContent(addon_handle, "episodes")
# id = ''.join(args.get('id', ""))
# content = cache.cacheFunction(getContent)
# getCategories(content, id)

# xbmcplugin.endOfDirectory(addon_handle)
# # Media Info View
# xbmc.executebuiltin('Container.SetViewMode(504)')
