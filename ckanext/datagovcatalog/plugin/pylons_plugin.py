"""
Mixin for Pylons-specific functionality. This aides the migration between Pylons and Flask.
"""
import ckan.plugins as p


class MixinPlugin(object):

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, '../templates')
        p.toolkit.add_resource('../fanstatic', 'datagovcatalog')

    # ITemplateHelpers
    def get_helpers(self):
        from ckanext.datagovcatalog.helpers import sitemap

        return {
            'get_sitemap_url': sitemap.get_sitemap_url,
        }
