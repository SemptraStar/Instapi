import requests
import json

import urllib
from urllib.request import urlopen
from requests_oauth2 import OAuth2


class Instapi():
    def __init__(self, client_id, client_secret, redirect_uri, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token

        self.user = user(self.access_token)
        self.tags = tags(self.access_token)
        self.media = media(self.access_token)
        self.images = images()

class user(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def self(self):
        """
        Get information about the owner of the access_token. 
        """

        url = "https://api.instagram.com/v1/users/self/?access_token=" + self.access_token
        request = requests.get(url)
        return request.json()

    def id(self, user_id):
        """
        Get information about a user.
        The public_content scope is required if the user is not the owner of the access_token. 

        Requirements
        Scope: public_content
        """

        url = "https://api.instagram.com/v1/users/{0}/?access_token={1}".format(user_id, self.access_token)
        request = requests.get(url)
        return request.json()

    def search(self, query, count = None):
        """
        Get a list of users matching the query. 

        Requirements
        Scope: public_content

        Parameters
        query 	        A query string.
        count 	        Number of users to return.
        """

        url = "https://api.instagram.com/v1/users/search?q={0}&access_token={1}".format(query, self.access_token)

        if count != None:
            url += "&count=" + str(count)

        request = requests.get(url)
        return request.json()

    def follows(self, user_id):
        """
        Get the list of users this user follows.

        Requirements
        Scope: follower_list

        Parameters
        user_id 	A valid user id.

        """

        url = "https://api.instagram.com/v1/users/{0}/follows?access_token={1}".format(user_id, self.access_token)

        request = requests.get(url)
        return request.json()
    def followed_by(self, user_id):
        """
        Get the list of users this user is followed by. 

        Requirements
        Scope: follower_list

        Parameters
        user_id 	A valid user id.

        """

        url = "https://api.instagram.com/v1/users/{0}/followed-by?access_token={1}".format(user_id, self.access_token)

        request = requests.get(url)
        return request.json()
    def relationship(self, user_id):
        """
        Get information about a relationship to another user. Relationships are expressed using the following terms in the response:

        outgoing_status: Your relationship to the user. Can be 'follows', 'requested', 'none'.
        incoming_status: A user's relationship to you. Can be 'followed_by', 'requested_by', 'blocked_by_you', 'none'.
 
        Requirements
        Scope: follower_list

        Parameters
        user_id 	A valid user id.

        """

        url = "https://api.instagram.com/v1/users/{0}/relationship?access_token={1}".format(user_id, self.access_token)

        request = requests.get(url)
        return request.json()

    def get_user_id(self, user):
        """
        Get an ID for the first found user.
        
        Requirements
        Scope: public_content

        Parameters
        user        User nickname
        """

        found_user = self.search(user)

        if found_user:
            return found_user["data"][0]["id"]
        else:
            raise UserNotFound("User " + user + " not found.")

class tags(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def search(self, tag):
        """
        Search for tags by name. 

        Requirements
        Scope: public_content 

        Parameters
        tag 	A valid tag name without a leading #. (eg. snowy, nofilter)
        """

        url = "https://api.instagram.com/v1/tags/search?q={0}&access_token={1}".format(tag, self.access_token)
        request = requests.get(url)
        return request.json()

    def info(self, tag):
        """
        Get information about a tag object.

        Requirements
        Scope: public_content

        Parameters
        tag 	A valid tag name without a leading #. (eg. snowy, nofilter)
        """

        url = "https://api.instagram.com/v1/tags/{0}?access_token={1}".format(tag, self.access_token)
        request = requests.get(url)
        print(request.headers)
        return request.json()

    def recent_media(self, tag, max_tag_id = None, min_tag_id = None, count = 10):
        """
        Get a list of recently tagged media.

        Requirements
        Scope: public_content

        Parameters
        tag 	    A valid tag name without a leading #. (eg. snowy, nofilter)
        max_tag_id 	Return media after this max_tag_id. (optional)
        min_tag_id 	Return media before this min_tag_id. (optional)
        count 	    Count of tagged media to return. (default = 10)
        """

        url = "https://api.instagram.com/v1/tags/{0}/media/recent?access_token={1}".format(tag, self.access_token)

        if max_tag_id:
            url += "&max_tag_id=" + str(max_tag_id)
        if min_tag_id:
            url += "&min_tag_id=" + str(min_tag_id)

        request = requests.get(url)
        return request.json()

class media(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def self_media(self):
        """
        Get the most recent media published by the owner of the access_token.

        Parameters
        max_id 	Return media earlier than this max_id.
        min_id 	Return media later than this min_id.
        count 	Count of media to return.
        """

        url = "https://api.instagram.com/v1/users/self/media/recent/?access_token={0}".format(self.access_token)
        request = requests.get(url)
        return request.json()

    def user_media(self, user = "", id = "", count = 20):
        """
        Get the most recent media published by a user.
        The public_content scope is required if the user is not the owner of the access_token. 
        You could specify user by his nickname or id.
        If user arg is given, make a search using user nickname.
        If id arg is given, make a search using user id.

        Requirements
        Scope: public_content

        Parameters
        user    User nickname
        id      User ID
        count 	Count of media to return.
        """

        if user:
            url = "https://api.instagram.com/v1/users/search?q={0}&access_token={1}".format(user, self.access_token)
            id = requests.get(url).json()["data"][0]["id"]

        url = "https://api.instagram.com/v1/users/{0}/media/recent/?access_token={1}&count={2}".format(id, self.access_token, count)

        data = []

        while True: 
            request = requests.get(url).json()
      
            data.extend(request["data"])
            count -= len(request["data"])

            if not request["pagination"] or count <= 0:
                return data

            url = request["pagination"]["next_url"]
        
    def info(self, media_id = "", shortcode = ""):
        """
        Get information about a media object. 
        Use the type field to differentiate between image and video media in the response. 
        You will also receive the user_has_liked field which tells you whether the owner of the access_token has liked this media.
        The public_content permission scope is required to get a media that does not belong to the owner of the access_token.
        
        Requirements
        Scope: public_content
        
        Parameters
        media_id 	A valid media id code.
        shortcode   A valid media shortcode.
        """

        if media_id:
            url = "https://api.instagram.com/v1/media/{0}?access_token={1}".format(media_id, self.access_token)
        else:
            url = "https://api.instagram.com/v1/media/{0}/D?access_token={1}".format(shortcode, self.access_token)
            request = requests.get(url)
            return request.content

        request = requests.get(url)
        return request.json()

    def likes(self, media_id):
        """
        Get a list of users who have liked this media.
        The public_content scope is required for media that does not belong to the owner of the access_token.

        Requirements
        Scope: public_content

        Parameters
        media_id 	A valid media id.
        """

        url = "https://api.instagram.com/v1/media/{0}/likes?access_token={1}".format(media_id, self.access_token)
        request = requests.get(url)

        return request.json()

    def comments(self, media_id):
        """
        Get a list of recent comments on a media object.
        The public_content scope is required for media that does not belong to the owner of the access_token. 

        Requirements
        Scope: public_content

        Parameters
        media_id 	A valid media id.
        """

        url = "https://api.instagram.com/v1/media/{0}/comments?access_token={1}".format(media_id, self.access_token)
        request = requests.get(url)

        return request.json()

class images():
    def __init__(self):
        pass

    def img_urls(self, media, type = "low_resolution"):
        """
        Get a dictionary with images id and url from list of media.

        Parameters
        media 	List of media objects
        type    ["thumbnail" | "low_resolution" | "standard_resolution"] - image size
        """

        imgs = {}

        for item in media:
            if item["type"] != "image":
                continue

            imgs[item["id"]] = item["images"][type]["url"]

        return imgs            
    
class UserNotFound(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def get_access_token(client_id = "", redirect_uri = "", scope = "basic public_content"):
    if not client_id:
        client_id = input("Enter your client id: ").strip()
    if not redirect_uri:
        redirect_uri = input("Enter your redirect uri: ").strip()
    if not scope:
        scope = input("Enter additional scope (left this blank for default): ")

    scope = scope.replace(" ", "+")

    url = "https://api.instagram.com/oauth/authorize/?client_id={0}&redirect_uri={1}&response_type=token".format(client_id, redirect_uri)

    if scope:
        url += "&scope=" + scope

    print("Copy and paste this link into your browser's query string:\n\n" + url)
    token = input("\nCopy the code from your query string and paste in here: ").strip()

    return token

