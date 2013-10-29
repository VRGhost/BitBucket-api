# -*- coding: utf-8 -*-

from . import base

class SSH(base.Endpoint):
    """ This class provide ssh-related methods to Bitbucket objects."""

    endpoints = {
        # SSH keys
        'GET_SSH_KEYS': 'ssh-keys/',
        'GET_SSH_KEY': 'ssh-keys/%(key_id)s',
        'SET_SSH_KEY': 'ssh-keys/',
        'DELETE_SSH_KEY': 'ssh-keys/%(key_id)s',
    }

    def all(self):
        """ Get all ssh keys associated with your account.
        """
        url = self.urls('GET_SSH_KEYS')
        return self.bitbucket.dispatch(url)

    def get(self, key_id=None):
        """ Get one of the ssh keys associated with your account.
        """
        url = self.urls('GET_SSH_KEY', key_id=key_id)
        return self.bitbucket.dispatch(url)

    def create(self, key=None, label="unnamed key"):
        """ Associate an ssh key with your account and return it.
        """
        key = str(key)
        url = self.urls('SET_SSH_KEY')
        return self.bitbucket.dispatch.post(url, data={"key": key, "label": label})

    def delete(self, key_id=None):
        """ Delete one of the ssh keys associated with your account.
            Please use with caution as there is NO confimation and NO undo.
        """
        url = self.urls('DELETE_SSH_KEY', key_id=key_id)
        return self.bitbucket.dispatch.delete(url, parse=False)
