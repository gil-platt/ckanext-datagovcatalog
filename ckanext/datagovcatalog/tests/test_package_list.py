# encoding: utf-8

"""Tests for tracking information."""

from ckan import model
from ckan import plugins as p
from ckan.lib.helpers import url_for
from ckanext.datagovcatalog.harvester.notifications import harvest_get_notifications_recipients
from ckantoolkit.tests import factories as ckan_factories
from ckantoolkit.tests.helpers import reset_db, FunctionalTestBase
from nose.tools import assert_in


class TestPackageList(FunctionalTestBase):

    @classmethod
    def setup_class(cls):
        super(TestPackageList, cls).setup_class()
        reset_db()
        
    def test_tracking_info(self):
        
        self._create_packages_and_tracking()
        app = self._get_test_app()
        res = app.get('/dataset')
        assert_in(self.package['name'], res.unicode_body)
        assert_in('recent views', res.unicode_body)

    def _create_packages_and_tracking(self):

        self.package = ckan_factories.Dataset()
        # add 12 visit to the dataset page
        url = url_for(controller='package', action='read',id=self.package['name'])
        app = self._get_test_app()
        for r in range(12):
            self._post_to_tracking(url=url, app=app, ip='199.200.100.{}'.format(r))
        
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