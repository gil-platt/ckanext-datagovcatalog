import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.datagovcatalog.harvester.notifications import harvest_get_notifications_recipients


log = logging.getLogger(__name__)


class DatagovcatalogPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datagovcatalog')
    
    def get_actions(self):
        return {
            'harvest_get_notifications_recipients': harvest_get_notifications_recipients
            }
    
    # ITemplateHelpers

    def get_helpers(self):
        from ckanext.datagovcatalog.helpers import sitemap

        return {
                'get_sitemap_url': sitemap.get_sitemap_url,
                }