# encoding: utf-8

"""Tests for notifications.py."""

from ckan import model
from ckan import plugins as p
from ckan.plugins import toolkit
from ckanext.datagovcatalog.harvester.notifications import harvest_get_notifications_recipients
from ckantoolkit.tests import factories as ckan_factories
from ckantoolkit.tests.helpers import reset_db
from nose.tools import assert_in


class TestExtraNotificationRecipients(object):

    @classmethod
    def setup_class(cls):
        if not p.plugin_loaded('harvest'):
            p.load('harvest')
        if not p.plugin_loaded('datagovcatalog'):
            p.load('datagovcatalog')
        reset_db()

    @classmethod
    def teardown_class(cls):
        p.unload('datagovcatalog')
        p.unload('harvest')
        reset_db()

    def test_get_extra_email_notification(self):
        context, source_id = self._create_harvest_source_with_owner_org_and_job_if_not_existing()

        new_rec_action = toolkit.get_action("harvest_get_notifications_recipients")
        new_recipients = new_rec_action(context, {'source_id': source_id})

        assert_in({'email': u'john@gmail.com', 'name': u'john@gmail.com'}, new_recipients)
        assert_in({'email': u'peter@gmail.com', 'name': u'peter@gmail.com'}, new_recipients)

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

        source_dict = {
            'title': 'Test Source 01',
            'name': 'test-source-01',
            'url': 'basic_test',
            'source_type': 'ckan',
            'owner_org': test_org['id'],
            'run': True
        }

        harvest_source = toolkit.get_action('harvest_source_create')(
                context.copy(),
                source_dict
            )
        
        return context, harvest_source['id']
