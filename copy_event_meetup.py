import urllib.request
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

# Get an access token at and fill in below
# https://secure.meetup.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=token&scope=event_management&redirect_uri=http://YOUR_WEBSITE 

token= "TOKEN_FROM_OAUTH_STEP"


fromgroup = "GROUP-NAME"
fromevent = "000000000"

togroups = {"THIS-GROUP", "THAT-GROUP"}
announce = "true"


for togroup in togroups:
    print(togroup)

    #getEvent
    url = "https://api.meetup.com/"+fromgroup+"/events/"+fromevent+"?&sign=true&photo-host=public&fields=featured_photo,plain_text_description"
    req = urllib.request.Request(url)

    ##parsing response
    r = urllib.request.urlopen(req).read()
    getEventJson = json.loads(r.decode('utf-8'))



    #getAlbums
    url = "https://api.meetup.com/"+togroup+"/photo_albums?&sign=true&photo-host=public&page=200"
    req = urllib.request.Request(url)

    ##parsing response
    r = urllib.request.urlopen(req).read()
    getAlbumsJson = json.loads(r.decode('utf-8'))

    ##Get album to insert picture. Usually named 'Meetup Group Photo Album'. Put in oldest album otherwise.
    albumid = getAlbumsJson[len(getAlbumsJson)-1]["id"]
    for album in getAlbumsJson:
        if album['title']=='Meetup Group Photo Album':
            albumid= album['id']

        



    try:
        description = getEventJson["plain_text_description"] #use plain text to avoid auto HTML
    except:
        description = ""

    try:
        duration = getEventJson["duration"]
    except:
        duration = ""

    try:
        how_to_find_us = getEventJson["how_to_find_us"]
    except:
        how_to_find_us = ""

    try:
        lat = getEventJson["venue"]["lat"]
    except:
        lat = ""

    try:
        lon = getEventJson["venue"]["lon"]
    except:
        lon = ""

    try:
        name = getEventJson["name"]
    except:
        name = ""

    try:
        time = getEventJson["time"]
    except:
        time = ""

    try:
        venue_id = getEventJson["venue"]["id"]
    except:
        venue_id = ""


    try:
        featured_photo_url = getEventJson["featured_photo"]["highres_link"]
    except:
        featured_photo_url = ""
        


    featurephoto = r"c:\YOUR_LOCAL_FOLDER\meetupFeaturePhoto.jpeg"

    #download feature photo
    if featured_photo_url != "":
        urllib.request.urlretrieve(featured_photo_url, featurephoto)



    ####multipart upload
    multipart_form_data = {
        'photo': ('custom_file_name.jpg', open(featurephoto, 'rb'))
        
        
    }

    #



    if featured_photo_url != "":
        photourl = "https://api.meetup.com/"+togroup+"/photo_albums/"+str(albumid)+"/photos?access_token="+token
        photoUpload = requests.post(photourl, files=multipart_form_data)

        #print(photoUpload.content)
        uploadPhotoJson = json.loads(photoUpload.content.decode("utf-8"))

        featured_photo_id= uploadPhotoJson["id"]
    else:
        featured_photo_id=""



    ##create meetup

    newEventParams = { "announce" : announce ,
               "description" : description,
               "duration": duration,
               "how_to_find_us": how_to_find_us,
               "name" : name,
               "time": time,
               "venue_id":venue_id,
               "featured_photo_id":featured_photo_id,
               "access_token":token
               
                       
        }


    postdata = urllib.parse.urlencode(newEventParams).encode("utf-8")

    posturl = "https://api.meetup.com/"+togroup+"/events"


    ##create new meetup
    request = urllib.request.Request(posturl, data=postdata) 
    response = urlopen(request)
    the_page = response.read()

    print(the_page)

