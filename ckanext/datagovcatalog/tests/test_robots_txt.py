from future import standard_library
from builtins import object
import logging
import pytest
import six
from urllib.parse import urljoin

from ckan.tests import helpers
from ckan.lib.base import config

standard_library.install_aliases()
log = logging.getLogger(__name__)


@pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_s3_url', 'https://test.gov/')
@pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_storage_path', 'test/sitemap')
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
        print(final_url)

        res = app.get('/robots.txt')
        if six.PY2:
            print(res.unicode_body)
            assert final_url in res
        else:
            print(res.body)
            assert final_url in res.body

        url1a = 'https://test2.gov/'
        url1b = 'test2/sitemap'
        config['ckanext.geodatagov.s3sitemap.aws_s3_url'] = url1a
        config['ckanext.geodatagov.s3sitemap.aws_storage_path'] = url1b
        final_url = urljoin(url1a, url1b, 'sitemap.xml')

        res = app.get('/robots.txt')
        if six.PY2:
            assert final_url in res
        else:
            assert final_url in res.body
