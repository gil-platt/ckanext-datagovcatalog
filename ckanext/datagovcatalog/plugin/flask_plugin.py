"""
Mixin for Flask-specific functionality. This aides the migration between Pylons and Flask.
"""
import ckan.plugins as p
from ckanext.datagovcatalog.helpers import sitemap


class MixinPlugin(object):

    sitemap.create_sitemap_url()

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_public_directory(config, '../public')

    # ITemplateHelpers
    def get_helpers(self):
        return {}
