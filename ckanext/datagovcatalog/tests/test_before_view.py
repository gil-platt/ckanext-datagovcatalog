from nose.tools import assert_equal, assert_not_in
from ckantoolkit.tests import factories
from ckan.tests import helpers
from ckanext.datagovcatalog.helpers.packages import update_tracking_info_to_package


class TestOverridePackage():

    def test_override_package(self):
        
        pkg_dict = {
            'name': 'dataset1',
            'organization': {
                'name': 'org1',
                'organization_type': 'Federal Government'
            },
            'resources': [
                {'url': 'http://resources.com/resouce1.json'},
                {'url': 'http://resources.com/resouce2.csv'},
                {'url': 'http://resources.com/resouce3.html'}
            ]
        }

        new_pkg_dict = {
            'name': 'dataset1',
            'organization': {
                'name': 'org1'
            },
            'tracking_summary': 'some tracking info',
            'resources': [
                {'url': 'http://resources.com/resouce1.json', 'tracking_summary': 'tracking info 1'},
                {'url': 'http://resources.com/resouce2.csv',  'tracking_summary': 'tracking info 2'},
                {'url': 'http://resources.com/resouce3.html', 'tracking_summary': 'tracking info 3'}
            ]
        }

        final_pkg = update_tracking_info_to_package(pkg_dict, new_pkg_dict)

        assert_equal(final_pkg['tracking_summary'], 'some tracking info')
        assert_equal(final_pkg['organization']['organization_type'], 'Federal Government')

        asserts = 0
        for resource in final_pkg['resources']:
            if resource['url'] == 'http://resources.com/resouce1.json':
                assert_equal(resource['tracking_summary'], 'tracking info 1')
                asserts += 1
            elif resource['url'] == 'http://resources.com/resouce2.csv':
                assert_equal(resource['tracking_summary'], 'tracking info 2')
                asserts += 1
            elif resource['url'] == 'http://resources.com/resouce3.html':
                assert_equal(resource['tracking_summary'], 'tracking info 3')
                asserts += 1

        assert_equal(asserts, 3)

    @helpers.change_config('ckanext.datagovcatalog.add_packages_tracking_info', 'false')
    def test_disable_tracking(self):
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'])
        context = {'ignore_auth': True}
        dataset_show = helpers.call_action(
            "package_show",
            context=context,
            id=dataset['name']
        )

        assert_not_in('tracking_summary', dataset_show)
