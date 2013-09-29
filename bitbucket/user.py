import functools

from . import base

def cachedProp(func):

    attrName = "_cache_for_%r_%i".format(func.__name__, id(func))
    @functools.wraps(func)
    def _wrapper(self):
        try:
            return self.__dict__[attrName]
        except KeyError:
            rv = func(self)
            self.__dict__[attrName] = rv
            return rv

    return property(_wrapper)

class SelfUser(base.Endpoint):

    endpoints = {
        "PROFILE": "user/",
        "PRIVILEGES": "user/privileges",
        "FOLLOWS": "user/follows",
        "REPOS": "user/repositories",
        "REPOS_FOLLOWS": "user/repositories/overview",
        "REPOS_DASHBOARD": "user/repositories/dashboard",
    }

    def profile(self):
        return self.bitbucket.dispatch(self.urls("PROFILE"))

    def priveleges(self):
        return self.bitbucket.dispatch(self.urls("PRIVILEGES"))

    def followsRepos(self):
        """List of repos that this account follows."""
        return self.bitbucket.dispatch(self.urls("REPOS_FOLLOWS"))

    def repositories(self):
        """List of repos visible to an account."""
        return self.bitbucket.dispatch(self.urls("REPOS"))

    def dashboard(self):
        """List of repos on the dashboard."""
        return self.bitbucket.dispatch(self.urls("REPOS_DASHBOARD"))

    def update(self, **kwargs):
        """Update user params."""
        return self.bitbucket.dispatch.put(self.urls("REPOS_DASHBOARD"), data=kwargs)

    @cachedProp
    def username(self):
        return self.profile()["user"]["username"]

class OtherUser(base.Endpoint):

    username = None
    
    def __init__(self, bitbucket, username):
        super(OtherUser, self).__init__(bitbucket)
        self.username = username

class Accessor(base.Element):

    self = None # Pointer to the current user object

    def __init__(self, *args, **kwargs):
        super(Accessor, self).__init__(*args, **kwargs)
        self.current = SelfUser(self.bitbucket)

    def getUser(self, username):
        return OtherUser(self.bitbucket, username)

    @property
    def self(s):
        return SelfUser(s.bitbucket)