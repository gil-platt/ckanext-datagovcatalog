from future import standard_library
standard_library.install_aliases()
from builtins import object
import logging
from urllib.parse import urljoin
from ckan import plugins

from ckan.tests import helpers
from ckan.lib.base import config

log = logging.getLogger(__name__)


class TestRobotsTxt(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_dynamic_robots_txt(self):
        
        app = helpers._get_test_app()
        
        url1a = 'https://test.gov/'
        url1b = 'test/sitemap'
        config['ckanext.geodatagov.s3sitemap.aws_s3_url'] = url1a
        config['ckanext.geodatagov.s3sitemap.aws_storage_path'] = url1b
        final_url = urljoin(url1a, url1b, 'sitemap.xml')

        res = app.get('/robots.txt')
        assert final_url in res
        
        url1a = 'https://test2.gov/'
        url1b = 'test2/sitemap'
        config['ckanext.geodatagov.s3sitemap.aws_s3_url'] = url1a
        config['ckanext.geodatagov.s3sitemap.aws_storage_path'] = url1b
        final_url = urljoin(url1a, url1b, 'sitemap.xml')

        res = app.get('/robots.txt')
        assert final_url in res
        
