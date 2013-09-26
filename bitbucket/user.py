from . import base

class UserBase(base.Endpoint):
    
    endpointBase = None

    def __init__(self, *args, **kwargs):
        self.endpoints = endp = {}
        for (name, postfix) in {
            "BASE_INFO": ""
        }.iteritems():
            endp[name] = self.endpointBase + postfix

        super(UserBase, self).__init__(*args, **kwargs)

    def info(self):
        print self.bitbucket.dispatch(self.urls("BASE_INFO"))
        1/0

class SelfUser(UserBase):

    endpointBase = "user"

class OtherUser(UserBase):

    endpointBase = "users"

class Accessor(base.Element):

    @property
    def self(s):
        return SelfUser(s.bitbucket)