# -*- coding: utf-8 -*-
# git+git://github.com/Sheeprider/BitBucket-api.git

__all__ = ['Bitbucket', ]

from urlparse import parse_qs
import json
import re

from requests import Request, Session
from requests_oauthlib import OAuth1
import requests

from . import (
    base,
    exceptions,
    issue,
    repository,
    service,
    ssh,
    user,
)

class Bitbucket(object):
    """ This class lets you interact with the bitbucket public API. """

    access_token = access_token_secret = None

    urls = base.URLs({
        # Get user profile and repos
        'GET_USER': 'users/%(username)s/',
        # Search repo
        # 'SEARCH_REPO': 'repositories/?name=%(search)s',
        # Get tags & branches
        'GET_TAGS': 'repositories/%(username)s/%(repo_slug)s/tags/',
        'GET_BRANCHES': 'repositories/%(username)s/%(repo_slug)s/branches/',

        'REQUEST_TOKEN': 'oauth/request_token/',
        'ACCESS_TOKEN': 'oauth/access_token/'
    })

    def __init__(self, consumer_key, consumer_secret):
        super(Bitbucket, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.repository = repository.Repository(self)
        self.service = service.Service(self)
        self.ssh = ssh.SSH(self)
        self.issue = issue.Issue(self)
        self.users = user.Accessor(self)
        self.oauth = None

    #  ========================
    #  = Oauth authentication =
    #  ========================

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
            raise exceptions.AuthError(r.content)
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
        self.oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret
        )

    #  ======================
    #  = High lvl functions =
    #  ======================

    def dispatch(self, url, method="GET", params=None, parse=True, **kwargs):
        """ Send HTTP request, with given method,
            credentials and data to the given URL,
            and return the success and the result on success.
        """
        assert self.oauth, "Must be autorised."
        
        r = Request(
            method=method,
            url=url,
            auth=self.oauth,
            params=params,
            data=kwargs)
        s = Session()
        resp = s.send(r.prepare())
        status = resp.status_code
        text = resp.text
        error = resp.reason
        print (text, error)
        if status >= 200 and status < 300:
            if parse:
                return json.loads(text)
            else:
                return text
        elif status >= 300 and status < 400:
            raise exceptions.DispatchError(
                'Unauthorized access, please check your credentials.',
                url, error, status
            )
        elif status >= 400 and status < 500:
            raise exceptions.DispatchError('Service not found.', url, error, status)
        elif status >= 500 and status < 600:
            raise exceptions.DispatchError('Server error.', url, error, status)
        else:
            raise exceptions.DispatchError(error, url, error, status)