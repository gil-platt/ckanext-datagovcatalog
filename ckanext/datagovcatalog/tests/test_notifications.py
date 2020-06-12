# encoding: utf-8

"""Tests for notifications.py."""

from ckan import model
from ckan import plugins as p
from ckan.plugins import toolkit
from ckanext.datagovcatalog.harvester.notifications import get_extra_notification_recipients
from ckantoolkit.tests import factories as ckan_factories
from ckantoolkit.tests.helpers import reset_db
from nose.tools import assert_equal


class TestExtraNotificationRecipients(object):

    @classmethod
    def setup_class(cls):
        if not p.plugin_loaded('harvest'):
            p.load('harvest')
        if not p.plugin_loaded('datagovcatalog'):
            p.load('datagovcatalog')
        if not p.plugin_loaded('test_nose_action_harvester'):
            p.load('test_nose_action_harvester')
        reset_db()

    @classmethod
    def teardown_class(cls):
        p.unload('datagovcatalog')
        p.unload('harvest')
        p.unload('test_nose_action_harvester')
        reset_db()

    def test_get_extra_email_notification(self):
        context, source_id = self._create_harvest_source_with_owner_org_and_job_if_not_existing()

        new_recipients = get_extra_notification_recipients(context, {'source_id': source_id})

        assert_equal(new_recipients, [{'email': u'john@gmail.com', 'name': u'john@gmail.com'},
                                      {'email': u'peter@gmail.com', 'name': u'peter@gmail.com'}])

    def _create_harvest_source_with_owner_org_and_job_if_not_existing(self):
        site_user = toolkit.get_action('get_site_user')(
            {'model': model, 'ignore_auth': True}, {})['name']

        context = {
            'user': site_user,
            'model': model,
            'session': model.Session,
            'ignore_auth': True,
        }

        test_org = ckan_factories.Organization(extras=[{'key': 'email_list', 'value': 'john@gmail.com, peter@gmail.com'}])
        test_other_org = ckan_factories.Organization()
        org_admin_user = ckan_factories.User()
        org_member_user = ckan_factories.User()
        other_org_admin_user = ckan_factories.User()

        toolkit.get_action('organization_member_create')(
            context.copy(),
            {
                'id': test_org['id'],
                'username': org_admin_user['name'],
                'role': 'admin'
            }
        )

        toolkit.get_action('organization_member_create')(
            context.copy(),
            {
                'id': test_org['id'],
                'username': org_member_user['name'],
                'role': 'member'
            }
        )

        toolkit.get_action('organization_member_create')(
            context.copy(),
            {
                'id': test_other_org['id'],
                'username': other_org_admin_user['name'],
                'role': 'admin'
            }
        )

        source_dict = {
            'title': 'Test Source',
            'name': 'test-source',
            'url': 'basic_test',
            'source_type': 'test-for-action-nose',
            'owner_org': test_org['id'],
            'run': True
        }

        try:
            harvest_source = toolkit.get_action('harvest_source_create')(
                context.copy(),
                source_dict
            )
        except toolkit.ValidationError:
            harvest_source = toolkit.get_action('harvest_source_show')(
                context.copy(),
                {'id': source_dict['name']}
            )
            pass

        return context, harvest_source['id']
