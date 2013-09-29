# -*- coding: utf-8 -*-
# git+git://github.com/Sheeprider/BitBucket-api.git

__all__ = ['Bitbucket', ]

from urlparse import parse_qs

from requests_oauthlib import OAuth1
import requests

from . import (
    base,
    dispatch,
    exceptions,
    issue,
    repository,
    service,
    ssh,
    user,
)

class BitbucketBase(object):
    """ This class lets you interact with the bitbucket public API. """

    auth = None
    user = property(lambda s: s.users.current) # Pointer to the current user object.

    def __init__(self):
        super(BitbucketBase, self).__init__()
        self.dispatch = dispatch.Dispatch(self)
        
        self.repository = repository.Repository(self)
        self.service = service.Service(self)
        self.ssh = ssh.SSH(self)
        self.issue = issue.Issue(self)
        self.users = user.Accessor(self)

    #  ======================
    #  = High lvl functions =
    #  ======================



class BitbucketOAuth(BitbucketBase):
    
    access_token = access_token_secret = None

    urls = base.URLs({
        'REQUEST_TOKEN': 'oauth/request_token/',
        'ACCESS_TOKEN': 'oauth/access_token/'
    })

    def __init__(self, consumer_key, consumer_secret):
        super(BitbucketOAuth, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def authorize(self, callback_url):
        """ Call this with your consumer key, secret and callback URL, to generate a token for verification. """
        if not callback_url:
            return exceptions.BitbucketError("Callback URL required")

        oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            callback_uri=callback_url
        )
        r = requests.post(self.urls('REQUEST_TOKEN'), auth=oauth)
        if r.status_code != 200:
            raise exceptions.AuthError((r.content, r.text))
        creds = parse_qs(r.content)

        self.access_token = creds.get('oauth_token')[0]
        self.access_token_secret = creds.get('oauth_token_secret')[0]

        return (self.access_token, self.access_token_secret)

    def verify(self, verifier, access_token=None, access_token_secret=None):
        """ After converting the token into verifier, call this to finalize the authorization. """
        if access_token:
            self.access_token = access_token
        if access_token_secret:
            self.access_token_secret = access_token_secret

        # Stored values can be supplied to verify
        oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            verifier=verifier
        )
        r = requests.post(self.urls('ACCESS_TOKEN'), auth=oauth)
        if r.status_code != 200:
            raise exceptions.AuthError(r.content)

        creds = parse_qs(r.content)
        self.finalize_oauth(creds.get('oauth_token')[0], creds.get('oauth_token_secret')[0])

    def finalize_oauth(self, access_token, access_token_secret):
        """ Called internally once auth process is complete. """
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Final OAuth object
        self.auth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret
        )

class BitbucketLoginPass(BitbucketBase):
    
    def __init__(self, login, password):
        super(BitbucketLoginPass, self).__init__()
        self.auth = (login, password)