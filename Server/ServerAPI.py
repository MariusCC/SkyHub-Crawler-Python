import requests  # Tutorial based on http://docs.python-requests.org/en/master/user/advanced/

from Server.UsersTable import getUser
from Crawler.Helpers.LinksHelper import LinksHelper
import ujson

session = requests.Session()
userLoggedIn = None
#url = "http://skyhub.me:4000/api/"
url = "http://127.0.0.1:4000/api/"

class ServerAPI:
    def __init__(self):
        pass

    @staticmethod
    def loginUser(user):

        user = getUser(user)
        if user is None:
            return False

        global userLoggedIn
        if (userLoggedIn is not None) and ((userLoggedIn['username'] == user['username'])or(userLoggedIn['id'] == user['id'])):
            print("User Already logged in")
            return userLoggedIn
        print("Loggin user")

        data = {
            'emailUsername': user['username'],
            'password': user['password']
        }

        headers = {}

        result = session.get(url+"auth/login", data=data, headers=headers)
        result = result.json()
        print(result)
        if result['result'] == True:
            print("User Logged In ", result['user']['id'])
            user['id'] = result['user']['id']
            user['sessionId'] = result['sessionId']
            userLoggedIn = user
            return user
        return None

    @staticmethod
    def postAddForum(user, parentId, name, title, description, iconPic, coverPic, arrKeywords = [],  dtOriginalDate = None, country='', city='', language='',  latitude=-666, longitude=-666):

        user = ServerAPI.loginUser(user)

        if user is None: return False

        title = LinksHelper.fixArchiveStrings(title)
        description = LinksHelper.fixArchiveStrings(description)
        iconPic = LinksHelper.fixArchiveStrings(iconPic)
        coverPic = LinksHelper.fixArchiveStrings(coverPic)

        rez = ServerAPI.processLocation(country, city, language, latitude, longitude)
        latitude = rez[0]
        longitude = rez[1]

        arrAdditionalInfo = {
            'scraped':True,
        }

        if dtOriginalDate is not None: arrAdditionalInfo['dtOriginal'] = dtOriginalDate

        if isinstance(arrKeywords, str): keywords = arrKeywords
        else: keywords = ','.join(str(e) for e in arrKeywords)

        data = {
            'id': user['id'],
            'sessionId': user['sessionId'],

            'parent': parentId,
            'title': title,
            'name': name,
            'description': description,
            'iconPic': iconPic,
            'coverPic': coverPic,
            'keywords': keywords,
            'country': country,
            'city': city,
            'language': language,
            'latitude': latitude,
            'longitude': longitude,
            'additionalInfo': ujson.dumps(arrAdditionalInfo)
        }

        headers = {}

        result = LinksHelper.getRequestTrials(session, url + "forums/add-forum", data, headers, maxTrials = 5)
        result = result.json()
        #print(result)
        if result['result'] == True:
            print('FORUM new ', result['forum']['URL'])
            return result['forum']['id']
        return None

    @staticmethod
    def postAddTopic(user, parentId, title, description, shortDescription='', arrKeywords=[], arrAttachments=[],
                     dtOriginalDate=None, country='', city='', language='', latitude=-666, longitude=-666,
                     authorName='', authorAvatar=''):
        user = ServerAPI.loginUser(user)

        if user is None: return False

        title = LinksHelper.fixArchiveStrings(title)
        description = LinksHelper.fixArchiveStrings(description)
        shortDescription = LinksHelper.fixArchiveStrings(shortDescription)
        authorAvatar = LinksHelper.fixArchiveStrings(authorAvatar)
        authorName = LinksHelper.fixArchiveStrings(authorName)

        rez = ServerAPI.processLocation(country, city, language, latitude, longitude)
        latitude = rez[0]
        longitude = rez[1]

        arrAdditionalInfo = {
            'scraped': True,
        }

        if dtOriginalDate is not None: arrAdditionalInfo['dtOriginal'] = dtOriginalDate
        if authorName != '': arrAdditionalInfo['orgName'] = authorName
        if authorAvatar != '': arrAdditionalInfo['orgAvatar'] = authorAvatar

        if isinstance(arrKeywords, str):
            keywords = arrKeywords
        else:
            keywords = ','.join(str(e) for e in arrKeywords)

        data = {
            'id': user['id'],
            'sessionId': user['sessionId'],

            'parent': parentId,
            'title': title,
            'description': description,
            'shortDescription': shortDescription,
            'keywords': keywords,
            'attachments': arrAttachments,
            'country': country,
            'city': city,
            'language': language,
            'latitude': latitude,
            'longitude': longitude,
            'additionalInfo': ujson.dumps(arrAdditionalInfo)
        }

        headers = {}

        result = LinksHelper.getRequestTrials(session, url + "topics/add-topic", data, headers, maxTrials = 5)
        result = result.json()

        # print(result)
        if result['result'] == True:
            print('topic new ', result['topic']['URL'])
            return result['topic']['id']
        return None

    @staticmethod
    def postAddReply(user, parentId, parentReplyId, title, description, arrKeywords = [], arrAttachments=[], dtOriginalDate = None, country='', city='', language='',  latitude=-666, longitude=-666, authorName='', authorAvatar='' ):

        user = ServerAPI.loginUser(user)

        if user is None: return False
        if parentId is None: return False
        if parentReplyId is None: parentReplyId = ""

        title = LinksHelper.fixArchiveStrings(title)
        description = LinksHelper.fixArchiveStrings(description)
        authorAvatar = LinksHelper.fixArchiveStrings(authorAvatar)
        authorName = LinksHelper.fixArchiveStrings(authorName)

        rez = ServerAPI.processLocation(country, city, language, latitude, longitude)
        latitude = rez[0]
        longitude = rez[1]

        arrAdditionalInfo = {
            'scraped':True,
        }

        if dtOriginalDate is not None: arrAdditionalInfo['dtOriginal'] = dtOriginalDate
        if authorName != '': arrAdditionalInfo['orgName'] = authorName
        if authorAvatar != '': arrAdditionalInfo['orgAvatar'] = authorAvatar

        if isinstance(arrKeywords, str): keywords = arrKeywords
        else: keywords = ','.join(str(e) for e in arrKeywords)

        data = {
            'id': user['id'],
            'sessionId': user['sessionId'],

            'parent': parentId,
            'parentReply': parentReplyId,
            'title': title,
            'description': description,
            'keywords': keywords,
            'attachments': arrAttachments,
            'country': country,
            'city': city,
            'language': language,
            'latitude': latitude,
            'longitude': longitude,
            'additionalInfo': ujson.dumps(arrAdditionalInfo)
        }

        headers = {}

        result = LinksHelper.getRequestTrials(session, url + "replies/add-reply", data, headers, maxTrials = 5)
        result = result.json()

        #print(result)
        if result['result'] == True:
            print('reply new ', result['reply']['URL'])
            return result['reply']['id']
        return None

    @staticmethod
    def processLocation(country, city, language, latitude, longitude):
        if ((country or language) != '') or (city != ''):
            location = ServerAPI.getAddress(city, (country or language))
            if location is not None:
                latitude = location['lat']
                longitude = location['lng']

        return [latitude, longitude]

    @staticmethod
    def getAddress(city, country):
        address = city + ' ' + country
        address = address.replace(' ', '+')

        session = requests.Session()
        result = LinksHelper.getRequestTrials(session, 'https://maps.google.com/maps/api/geocode/json?address='+address+'&sensor=false', {}, {}, maxTrials=5)
        result = result.json()
        if len(result['results']) > 0:
            result =result['results'][0]['geometry']['location']
        else:
            result = None
        return result



