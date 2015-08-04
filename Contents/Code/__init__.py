import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup

NAME = "Chiasenhac"
BASE_URL = "http://chiasenhac.com/"
SEARH_URL = 'http://search.chiasenhac.com/search.php?s=%s'
DEFAULT_ICO = 'icon-default.png'
SEARCH_ICO = 'icon-search.png'
NEXT_ICO = 'icon-next.png'
ART = 'art-default.png'
# #### REGEX #####
RE_MENU = Regex('<div id="myslidemenu"(.+?)<br style="clear:')
RE_INDEX = Regex('<div class="m-left">(.+?)<div class="main-right">')
RE_PAGE = Regex('<div class="padding">(.+?)</div>')
RE_INDEX_SEARCH = Regex('<div class="m-left">(.+?)<div class="main-right">')
# ###################################################################################################

def Start():
    ObjectContainer.title1 = NAME
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(DEFAULT_ICO)
    DirectoryObject.art = R(ART)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'
    HTTP.Headers['X-Requested-With'] = 'XMLHttpRequest'


####################################################################################################
@handler('/video/chiasenhac', NAME, art=ART, thumb=DEFAULT_ICO)
def MainMenu():
    oc = ObjectContainer()
    oc.add(InputDirectoryObject(
        key=Callback(Search),
        title='SEARCH'
    ))

    try:
        link = HTTP.Request(BASE_URL, cacheTime=3600).content
        newlink = ''.join(link.splitlines()).replace('\t', '')
        match = re.compile(RE_MENU).findall(newlink)
        soup = BeautifulSoup(str(match[0]))
        li_menu = soup('li')
        for i in range(1, len(li_menu)):
            lsoup = BeautifulSoup(str(li_menu[i]))
            ltitle = lsoup('a')[0]['title']
            llink = BASE_URL + lsoup('a')[0]['href']

            oc.add(DirectoryObject(
                key=Callback(Category, title=ltitle, catelink=llink),
                title=ltitle,
                thumb=R(DEFAULT_ICO)
            ))

    except Exception, ex:
        Log("******** Error retrieving and processing latest version information. Exception is:\n" + str(ex))

    return oc


####################################################################################################

@route('/video/chiasenhac/search')
def Search(query=None):
    if query is not None:
        url = SEARH_URL % (String.Quote(query, usePlus=True))
        return Index_search(query, url)


@route('/video/chiasenhac/index_search')
def Index_search(title, indexlink):
    oc = ObjectContainer(title2=title)
    link = HTTP.Request(indexlink, cacheTime=3600).content
    newlink = ''.join(link.splitlines()).replace('\t', '')
    match = re.compile(RE_INDEX_SEARCH).findall(newlink)
    soup = BeautifulSoup(str(match[0]))
    tenbh = soup('div', {'class': 'tenbh'})
    gen = soup('span', {'class': 'gen'})
    index = 0
    for t in tenbh:
        tsoup = BeautifulSoup(str(t))
        ttitle = tsoup('a')[0].contents[0]
        tlink = BASE_URL + tsoup('a')[0]['href']
        tartist = tsoup('p')[1].text
        try:
            info = BeautifulSoup(str(gen[index]))('span')[0].next.next.next.next
            if info == None:
                info = BeautifulSoup(str(gen[index]))('span')[0].next.next.next
            ttitle = '[' + info + '] - ' + ttitle.encode('utf8') + ' - ' + tartist.encode('utf-8')
            oc.add(createMediaObject(
                url=tlink,
                title=ttitle,
                thumb=R(DEFAULT_ICO),
                art=R(ART),
                rating_key=ttitle
            ))

        except:
            pass
        index += 1

    matchpages = re.compile(RE_PAGE).findall(newlink)
    soupli = BeautifulSoup(str(matchpages[0]))
    lipage = soupli('li')
    for l in lipage:
        try:
            l['class']  #active_page
        except KeyError:
            lsoup = BeautifulSoup(str(l))
            ltitle = lsoup('a')[0].contents[0]
            llink = lsoup('a')[0]['href']
            oc.add(DirectoryObject(
                key=Callback(Index_search, title=ltitle, indexlink=llink),
                title=ltitle,
                thumb=R(NEXT_ICO)
            ))

    return oc


@route('/video/chiasenhac/category')
def Category(title, catelink):
    oc = ObjectContainer(title2=title)
    link = HTTP.Request(catelink, cacheTime=3600).content
    newlink = ''.join(link.splitlines()).replace('\t', '')
    match = re.compile(RE_INDEX).findall(newlink)
    soup = BeautifulSoup(str(match[0]))
    gen = soup('div', {'class': 'list-r list-1'})
    if len(gen) > 0:
        for g in gen:
            gsoup = BeautifulSoup(str(g))
            gtitle = gsoup('a')[0]['title']
            glink = BASE_URL + gsoup('a')[0]['href']
            if str(gsoup('a')[0]).find('img') != -1:
                gimage = gsoup('img')[0]['src']
            else:
                gimage = R(DEFAULT_ICO)
            info = gsoup('span', {'style': 'color: red'})
            if len(info) > 0:
                infotext = info[0].text
                gtitle = '[' + infotext + '] - ' + gtitle
            oc.add(createMediaObject(
                url=glink,
                title=gtitle,
                thumb=gimage,
                art=R(ART),
                rating_key=gtitle
            ))

    gen = soup('div', {'class': 'list-l list-1'})
    if len(gen) > 0:
        for g in gen:
            gsoup = BeautifulSoup(str(g))
            gtitle = gsoup('a')[0]['title']
            glink = BASE_URL + gsoup('a')[0]['href']
            if str(gsoup('a')[0]).find('img') != -1:
                gimage = gsoup('img')[0]['src']
            else:
                gimage = R(DEFAULT_ICO)
            info = gsoup('span', {'style': 'color: red'})
            if len(info) > 0:
                infotext = info[0].text
                gtitle = '[' + infotext + '] - ' + gtitle
            oc.add(createMediaObject(
                url=glink,
                title=gtitle,
                thumb=gimage,
                art=R(ART),
                rating_key=gtitle
            ))

    else:
        gen = soup('div', {'class': 'text2'})
        if len(gen) <= 0:
            gen = soup('div', {'class': 'gensmall'})
        if len(gen) <= 0:
            gen = soup('span', {'class': 'gen'})

        for g in gen:
            try:
                gsoup = BeautifulSoup(str(g))
                if len(gsoup('a')) > 1:
                    gtitle = gsoup('a')[2]['title']
                    glink = BASE_URL + gsoup('a')[1]['href']
                    if str(gsoup('a')[0]).find('img') != -1:
                        gimage = gsoup('img')[0]['src']
                    else:
                        gimage = R(DEFAULT_ICO)
                else:
                    gtitle = gsoup('a')[0]['title']
                    glink = BASE_URL + gsoup('a')[0]['href']
                    if str(gsoup('a')[0]).find('img') != -1:
                        gimage = gsoup('img')[0]['src']
                    else:
                        gimage = R(DEFAULT_ICO)
                oc.add(createMediaObject(
                    url=glink,
                    title=gtitle,
                    thumb=gimage,
                    art=R(ART),
                    rating_key=gtitle
                ))

            except:
                pass
    try:
        matchpages = re.compile(RE_PAGE).findall(newlink)
        soupli = BeautifulSoup(str(matchpages[0]))
        lipage = soupli('li')
        for l in lipage:
            try:
                l['class']  #active_page
            except KeyError:
                lsoup = BeautifulSoup(str(l))
                ltitle = lsoup('a')[0].contents[0]
                llink = BASE_URL + lsoup('a')[0]['href']
                oc.add(DirectoryObject(
                    key=Callback(Category, title=ltitle, catelink=llink),
                    title=ltitle,
                    thumb=R(NEXT_ICO)
                ))
    except:
        pass

    return oc

####################################################################################################

@route('/video/chiasenhac/createMediaObject')
def createMediaObject(url, title, thumb, art, rating_key, include_container=False,includeRelatedCount=None,includeRelated=None,includeExtras=None):
    if str(url).find('/video/') == -1: #and Client.Product and Client.Product in ('Plex Web', 'Web Client', 'Plex for Android', 'Plex Home Theater') :
        Log('Play Audio: - '+title)
        Log(url)
        if Client.Product and Client.Product in ('Plex Web', 'Web Client', 'Plex Home Theater') :
            container = 'mp3'
            audio_codec = AudioCodec.MP3
            audio_channels = 2
            track_object = TrackObject(
                key=Callback(createMediaObject, url=url, title=title, thumb=thumb, art=art, rating_key=rating_key, include_container=True),
                title=title,
                thumb=thumb,
                art=art,
                rating_key=rating_key,
                items=[
                    MediaObject(
                        parts=[
                            PartObject(key=Callback(PlayVideo, url=url))
                            # PartObject(key=url)
                        ],
                        container=container,
                        audio_codec=audio_codec,
                        audio_channels=audio_channels,
                        optimized_for_streaming=True
                    )]
            )

        else:
            media_obj = MediaObject(
                audio_codec=AudioCodec.MP3,
                container='mp3'
            )
            track_object = TrackObject(
                key=Callback(createMediaObject, url=url, title=title, thumb=thumb, art=art, rating_key=rating_key, include_container=True),
                rating_key=rating_key
            )
            track_object.title = title
            track_object.thumb = thumb

            media_obj.add(PartObject(key=Callback(PlayAudio, url=url)))
            track_object.add(media_obj)
    else:
        Log('Play Video - '+title)
        container = Container.MP4
        video_codec = VideoCodec.H264
        audio_codec = AudioCodec.AAC
        audio_channels = 2
        track_object = EpisodeObject(
            key=Callback(
                createMediaObject,
                url=url,
                title=title,
                thumb=thumb,
                art=art,
                rating_key=rating_key,
                include_container=True
            ),
            title=title,
            thumb=thumb,
            art=art,
            rating_key=rating_key,
            items=[
                MediaObject(
                    parts=[
                        PartObject(key=Callback(PlayVideo, url=url))
                    ],
                    container=container,
                    video_codec=video_codec,
                    audio_codec=audio_codec,
                    audio_channels=audio_channels,
                    optimized_for_streaming=True
                )
            ]
        )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object

@route('video/chiasenhac/playaudio')
def PlayAudio(url):
    url = medialink(url)
    return Redirect(url)

@indirect
def PlayVideo(url):
    url = medialink(url)
    Log('File Link: '+url)
    return IndirectResponse(VideoClipObject, key=url)

def medialink(url):
    link = HTTP.Request(url, cacheTime=3600).content
    newlink = ''.join(link.splitlines()).replace('\t', '')
    mlink = urllib2.unquote(re.compile('"file": decodeURIComponent\("(.+?)"\),').findall(newlink)[0])
    return mlink

####################################################################################################
