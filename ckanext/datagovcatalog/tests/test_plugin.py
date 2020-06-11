# encoding: utf-8

'''Tests for the ckanext.datagovcatalog extension.'''

from nose.tools import assert_true
import ckan.plugins

class TestDatagovCatalogPluginLoaded(object):
    '''Tests for the ckanext.datagovcatalog.plugin module.'''

    @classmethod
    def setup_class(cls):
        ckan.plugins.load('datagovcatalog')
    
    @classmethod
    def teardown_class(cls):
        ckan.plugins.unload('datagovcatalog')

    def test_plugin_loaded(self):
        assert_true(ckan.plugins.plugin_loaded('datagovcatalog'))