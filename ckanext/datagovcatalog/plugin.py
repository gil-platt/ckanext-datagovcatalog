import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.datagovcatalog.harvester.notifications import get_extra_notification_recipients

log = logging.getLogger(__name__)


class DatagovcatalogPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datagovcatalog')
    
    def get_actions(self):
        return {
            'add_extra_notification_recipients': get_extra_notification_recipients
            }