# encoding: utf-8

"""Tests for notifications.py."""
import logging

from ckan import model
from ckan import plugins as p
from ckan.plugins import toolkit
from ckan.tests import helpers
import ckan.tests.factories as factories
from ckantoolkit.tests.helpers import reset_db

log = logging.getLogger(__name__)


class TestCollectionSearch(object):
    
    def setup(self):
        site_user = toolkit.get_action('get_site_user')(
            {'model': model, 'ignore_auth': True}, {})['name']

        self.context = {
            'user': site_user,
            'model': model,
            'session': model.Session,
            'ignore_auth': True,
        }

        self._create_datasets()

    def _create_datasets(self):
        """ create the required datasets to test """
        log.info('Creating datasets for testing collections')
        # create just one time
        if hasattr(self, 'org1'):
            return 
        reset_db  # TODO it's seems not working
        self.org1 = factories.Organization()
        log.info('Org1 created {}'.format(self.org1['id']))
        self.org2 = factories.Organization()
        log.info('Org2 created {}'.format(self.org2['id']))
        self.group1 = factories.Group()
        log.info('Group1 created {}'.format(self.group1['id']))
        self.group2 = factories.Group()
        log.info('Group2 created {}'.format(self.group2['id']))
        
        self.parent = factories.Dataset(owner_org=self.org1['id'],
                                             extras=[{'key': 'collection_metadata', 'value': 'true'}],
                                             title='The Father test_collections_unique',
                                             groups=[{'name': self.group1['name']}, {'name': self.group2['name']}])
        log.info('Parent created {}'.format(self.parent['id']))
        self.child1 = factories.Dataset(owner_org=self.org1['id'],
                                             extras=[{'key': 'collection_package_id', 'value': self.parent['id']}],
                                             title='The Child 2 test_collections_unique',
                                             groups=[{'name': self.group1['name']}])
        log.info('Child 1 created {}'.format(self.child1['id']))
        self.child2 = factories.Dataset(owner_org=self.org1['id'],
                                             extras=[{'key': 'collection_package_id', 'value': self.parent['id']}],
                                             title='The Child 2 test_collections_unique',
                                             groups=[{'name': self.group2['name']}])
        log.info('Child 2 created {}'.format(self.child2['id']))

    def test_not_children_in_package_search_results(self):

        res = helpers.call_action('package_search', q='test_collections_unique', context=self.context)
        log.info('package_search results count {}'.format(res['count']))

        for dataset in res['results']:
            # just parents
            title = dataset['title']
            log.info('Check dataset {}'.format(title))
            assert 'Child' not in title
            extra_keys = [extra['key'] for extra in dataset['extras']]
            assert 'collection_package_id' not in extra_keys

        # reset DB is failing so we count other tests parent packages
        # assert_equal(res['count'], 1)

    def test_org_and_group_count_datasets(self):
        log.info('Org1 test {}'.format(self.org1['id']))
        org1 = helpers.call_action("organization_show", context=self.context,
                                   id=self.org1['id'], include_dataset_count=True)
        assert org1['package_count'] == 1

        grp1 = helpers.call_action("group_show", context=self.context,
                                   id=self.group1['name'],
                                   include_dataset_count=True)
        assert grp1['package_count'] == 1

        grp2 = helpers.call_action("group_show", context=self.context,
                                   id=self.group2['name'],
                                   include_dataset_count=True)
        assert grp2['package_count'] == 1
