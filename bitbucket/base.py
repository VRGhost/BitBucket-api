from . import exceptions

class URLs(object):

    base = r"https://bitbucket.org/api/1.0/"

    def __init__(self, tails):
        super(URLs, self).__init__()
        self.tails = tails.copy()

    def __call__(self, tailName, **kwargs):
        tail = self.tails[tailName] % kwargs
        return self.base + tail

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.tails)

class Element(object):
    """Bitbucket sub-element."""

    bitbucket = None

    def __init__(self, bitbucket):
        super(Element, self).__init__()
        self.bitbucket = bitbucket

class Endpoint(Element):
    """Bitbucket API element/endpoint."""

    urls = endpoints = None

    def __init__(self, bitbucket):
        super(Endpoint, self).__init__(bitbucket)
        if not self.endpoints:
            raise exceptions.BitbucketError("Please set up API endpoints for this element.")
        self.urls = URLs(self.endpoints)