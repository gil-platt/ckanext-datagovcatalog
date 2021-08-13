import logging
from ckan.lib.base import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.datagovcatalog.harvester.notifications import harvest_get_notifications_recipients
from ckanext.datagovcatalog.helpers.packages import update_tracking_info_to_package


log = logging.getLogger(__name__)


class DatagovcatalogPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

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

    # # IPackageController

    def before_view(self, pkg_dict):

        print(pkg_dict)
        # Add tracking information just for datasets
        if pkg_dict.get('type', 'dataset') == 'dataset':
            if toolkit.asbool(config.get('ckanext.datagovcatalog.add_packages_tracking_info', True)):
                # add tracking information.
                # CKAN by default hide tracking info for datasets

                # The pkg_dict received here could include some custom data
                # (like organization_type from GeoDataGov extension)
                # just get this new data and merge witgh previous pkg_dict version
                new_pkg_dict = toolkit.get_action("package_show")({}, {
                    'include_tracking': True,
                    'id': pkg_dict['id']
                })

                pkg_dict = update_tracking_info_to_package(pkg_dict, new_pkg_dict)

            print(pkg_dict)
        return pkg_dict
