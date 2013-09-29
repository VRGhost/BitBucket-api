
import json

from requests import Request, Session

from . import exceptions

class Dispatch(object):

    def __init__(self, bitbucket):
        super(Dispatch, self).__init__()
        self.bitbucket = bitbucket

    def get(self, *args, **kwargs):
        return self.doRequest("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.doRequest("POST", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.doRequest("PUT", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.doRequest("DELETE", *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def doRequest(self, method, url, params=None, parse=True, data=None):
        """ Send HTTP request, with given method,
            credentials and data to the given URL,
            and return the success and the result on success.
        """
        if not self.bitbucket.auth:
            raise ValueError("No auth credentials.")

        if data:
            data = dict(data)
        else:
            data = {}
        
        r = Request(
            method=method,
            url=url,
            auth=self.bitbucket.auth,
            params=params,
            data=data
        )
        s = Session()
        resp = s.send(r.prepare())
        status = resp.status_code
        text = resp.text
        error = resp.reason
        if status >= 200 and status < 300:
            if parse:
                return json.loads(text)
            else:
                return text
        else:
            raise exceptions.DispatchError(text, url, error, status)