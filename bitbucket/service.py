# -*- coding: utf-8 -*-

from . import base

class Service(base.Endpoint):
    """ This class provide services-related methods to Bitbucket objects."""

    endpoints = {
        # Get services (hooks)
        'GET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
        'GET_SERVICES': 'repositories/%(username)s/%(repo_slug)s/services/',
        # Set services (hooks)
        'SET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/',
        'UPDATE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
        'DELETE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
    }

    def create(self, service, repo_slug=None, **kwargs):
        """ Add a service (hook) to one of your repositories.
            Each type of service require a different set of additionnal fields,
            you can pass them as keyword arguments (fieldname='fieldvalue').
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('SET_SERVICE', username=self.bitbucket.username, repo_slug=repo_slug)
        return self.bitbucket.dispatch.post(url, data=dict(type=service, data=kwargs))

    def get(self, service_id, repo_slug=None):
        """ Get a service (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_SERVICE', username=self.bitbucket.username, repo_slug=repo_slug, service_id=service_id)
        return self.bitbucket.dispatch(url)

    def update(self, service_id, repo_slug=None, **kwargs):
        """ Update a service (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('UPDATE_SERVICE', username=self.bitbucket.username, repo_slug=repo_slug, service_id=service_id)
        return self.bitbucket.dispatch.put(url, data=kwargs)

    def delete(self, service_id, repo_slug=None):
        """ Delete a service (hook) from one of your repositories.
            Please use with caution as there is NO confimation and NO undo.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('DELETE_SERVICE', username=self.bitbucket.username, repo_slug=repo_slug, service_id=service_id)
        return self.bitbucket.dispatch.delete(url)

    def all(self, repo_slug=None):
        """ Get all services (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_SERVICES', username=self.bitbucket.username, repo_slug=repo_slug)
        return self.bitbucket.dispatch(url)