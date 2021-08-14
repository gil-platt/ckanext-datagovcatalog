from future import standard_library
standard_library.install_aliases()

from builtins import object
import logging
import pytest
import six
from urllib.parse import urljoin

from ckan.tests import helpers
from ckan.lib.base import config

from ckanext.datagovcatalog.helpers import sitemap

log = logging.getLogger(__name__)


class TestRobotsTxt(object):

    @pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_s3_url', 'https://test.gov/')
    @pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_storage_path', 'test/sitemap')
    def test_dynamic_robots_txt(self):
        if six.PY3:
            sitemap.create_sitemap_url()

        app = helpers._get_test_app()

        url1a = 'https://test.gov/'
        url1b = 'test/sitemap'
        config['ckanext.geodatagov.s3sitemap.aws_s3_url'] = url1a
        config['ckanext.geodatagov.s3sitemap.aws_storage_path'] = url1b
        final_url = urljoin(url1a, url1b, 'sitemap.xml')

        res = app.get('/robots.txt')
        if six.PY2:
            assert final_url in res
        else:
            assert final_url in res.body

    @pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_s3_url', 'https://test2.gov/')
    @pytest.mark.ckan_config('ckanext.geodatagov.s3sitemap.aws_storage_path', 'test2/sitemap')
    def test_nondynamic_robots_txt(self):
        if six.PY3:
            sitemap.create_sitemap_url()

        app = helpers._get_test_app()

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
