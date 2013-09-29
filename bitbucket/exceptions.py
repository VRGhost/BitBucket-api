class BitbucketError(Exception):
    """Generic Bitbucket error."""

class AuthError(BitbucketError):
    """Authorisation error."""

class DispatchError(AuthError):

    def __init__(self, msg, url, reason, code):
        super(DispatchError, self).__init__("Error accessing %r:: return code: %s; reason: %r; message: %r." % (
            url, code, reason, msg
        ))
        self.msg = msg
        self.code = code
        self.url = url
        self.reason = reason