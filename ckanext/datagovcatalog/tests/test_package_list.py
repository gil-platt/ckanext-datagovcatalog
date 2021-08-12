# encoding: utf-8

"""Tests for tracking information."""
from datetime import datetime, timedelta
from ckan import model
from ckan import plugins as p
from ckan.lib.helpers import url_for
from ckan.lib.cli import Tracking, SearchIndexCommand
from ckanext.datagovcatalog.harvester.notifications import harvest_get_notifications_recipients
from ckantoolkit.tests import factories as ckan_factories
from ckan.tests import helpers

import pytest


# @pytest.fixture
@pytest.mark.usefixtures('with_request_context')
class TestPackageList(object):

    def setup(self):
        pass

    @helpers.change_config('ckanext.datagovcatalog.add_packages_tracking_info', 'true')
    def test_tracking_info(self, app):
        
        self.app = app
        # Create packages and navigate them
        self._create_packages_and_tracking()
        # update tracking info
        self._update_tracking_info()
        
        # ensure we can see tracking info
        res = self.app.get('/dataset')
        assert self.package['name'] in res.unicode_body
        assert 'recent views' in res.unicode_body

    def _create_packages_and_tracking(self):

        self.package = ckan_factories.Dataset()
        # add 12 visit to the dataset page
        url = url_for(controller='package', action='read',id=self.package['name'])
        for r in range(12):
            self._post_to_tracking(url=url, app=self.app, ip='199.200.100.{}'.format(r))
        
    def _update_tracking_info(self):
        # update tracking info
        date = (datetime.now() -timedelta(days=1)).strftime('%Y-%m-%d')
        Tracking('Tracking').update_all(engine=model.meta.engine, start_date=date)

        #rebuild search index
        class FakeOptions():
            def __init__(self,**kwargs):
                for key in kwargs:
                    setattr(self,key,kwargs[key])
        sic = SearchIndexCommand('search-index')
        sic.args = []
        sic.options = FakeOptions(only_missing=False, force=False, refresh=False, commit_each=False, quiet=False)
        sic.rebuild()
        
    def _post_to_tracking(self, app, url, type_='page', ip='199.204.138.90',
                          browser='firefox'):
        '''Post some data to /_tracking directly.
        This simulates what's supposed when you view a page with tracking
        enabled (an ajax request posts to /_tracking).
        '''

        params = {'url': url, 'type': type_}
        extra_environ = {
            # The tracking middleware crashes if these aren't present.
            'HTTP_USER_AGENT': browser,
            'REMOTE_ADDR': ip,
            'HTTP_ACCEPT_LANGUAGE': 'en',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
        }
        app.post('/_tracking', params=params, extra_environ=extra_environ)
