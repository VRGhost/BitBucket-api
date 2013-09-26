class BitbucketError(Exception):
    """Generic Bitbucket error."""

class AuthError(BitbucketError):
    """Authorisation error."""

class DispatchError(AuthError):

    def __init__(self, msg, url, reason, code):
        super(DispatchError, self).__init__("%s (url=%r code=%s reason=%r)" % (msg, url, code, reason))
        self.msg = msg
        self.code = code
        self.url = url
        self.reason = reason