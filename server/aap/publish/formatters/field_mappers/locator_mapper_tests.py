# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from apps.publish import init_app
from superdesk.tests import TestCase

from .locator_mapper import LocatorMapper


class SelectorcodeMapperTest(TestCase):

    desks = [{'_id': 1, 'name': 'National'},
             {'_id': 2, 'name': 'Sports'},
             {'_id': 3, 'name': 'Finance'}]

    article1 = {
        'subject': [{'qcode': '10006000'}, {'qcode': '15011002'}]

    }
    article2 = {
        'subject': [{'qcode': '15011002'}, {'qcode': '10006000'}]
    }
    article3 = {
        'subject': [{'qcode': '15063000'}, {'qcode': '15067000'}]

    }
    article4 = {
        'subject': [{'qcode': '9999999'}]

    }
    article5 = {
        'subject': [{'qcode': '15000000'}, {'qcode': '15063000'}]

    }

    article6 = {
        'subject': [{'qcode': '15011002'}, {'qcode': '10006000'}],
        'place': [{
            'name': 'NSW',
            'state': '',
            'world_region': 'Oceania',
            'group': 'Australia',
            'qcode': 'NSW',
            'country': 'Australia'
        }]
    }

    article7 = {
        'subject': [{'qcode': '15011002'}, {'qcode': '10006000'}],
        'place': [{
            'name': 'CHINA',
            'state': '',
            'world_region': 'China',
            'group': 'Rest of the World',
            'qcode': 'CHN',
            'country': 'China'
        }]
    }

    article8 = {
        'subject': [{'qcode': '10006000'}],
        'place': [{
            'name': 'CHINA',
            'state': '',
            'world_region': 'China',
            'group': 'Rest of the World',
            'qcode': 'CHN',
            'country': 'China'
        }]
    }
    category1 = 'I'
    category2 = 'D'
    categoryX = 'X'
    locator_map = LocatorMapper()
    vocab = [{'_id': 'categories', 'items': [
        {"is_active": True, "name": "Overseas Sport", "qcode": "S", "subject": "15000000"},
        {"is_active": True, "name": "Domestic Sport", "qcode": "T", "subject": "15000000"},
        {'is_active': True, 'name': 'Finance', 'qcode': 'F', 'subject': '04000000'},
        {'is_active': True, 'name': 'World News', 'qcode': 'I'},
        {"is_active": True, "name": "Entertainment", "qcode": "e", "subject": "01000000"},
        {"is_active": True, "name": "Australian General News", "qcode": "a"}
    ]}]

    def setUp(self):
        self.app.data.insert('desks', self.desks)
        self.app.data.insert('vocabularies', self.vocab)
        init_app(self.app)

    def test_locator_code_for_international_domestic_news(self):
        self.assertEqual(self.locator_map.map(self.article2, 'C'), 'TRAVI')
        self.assertEqual(self.locator_map.map(self.article6, 'C'), 'TRAVD')
        self.assertEqual(self.locator_map.map(self.article7, 'C'), 'TRAVI')

    def test_locator_code_for_international_domestic_sport(self):
        self.assertEqual(self.locator_map.map(self.article3, 'S'), 'VOL')
        self.assertEqual(self.locator_map.map(self.article3, 'T'), 'VOL')
        self.assertEqual(self.locator_map.map(self.article5, 'T'), 'TTEN')

    def test_locator_code_is_none(self):
        self.assertIsNone(self.locator_map.map(self.article4, self.category2))

    def test_headline_prefix(self):
        article = {
            'headline': 'This is test headline',
            'subject': [{'qcode': '15063000'}],
            'place': [{
                'name': 'NSW',
                'state': '',
                'world_region': 'Oceania',
                'group': 'Australia',
                'qcode': 'NSW',
                'country': 'Australia'
            }]
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'S'),
                         'TTEN:This is test headline')

    def test_headline_prefix_legacy(self):
        article = {
            'headline': 'VOL:This is test headline',
            'subject': [{'qcode': '15063000'}],
            'auto_publish': True,
            'place': [{
                'name': 'NSW',
                'state': '',
                'world_region': 'Oceania',
                'group': 'Australia',
                'qcode': 'NSW',
                'country': 'Australia'
            }]
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'S'),
                         'VOL:This is test headline')

    def test_headline_prefix_not_sports(self):
        article = {
            'headline': 'This is test headline',
            'subject': [{'qcode': '04001000'}],
            'place': [{
                'name': 'NSW',
                'state': '',
                'world_region': 'Oceania',
                'group': 'Australia',
                'qcode': 'NSW',
                'country': 'Australia'
            }]
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'A'),
                         'NSW:This is test headline')

    def test_headline_prefix_no_place(self):
        article = {
            'headline': 'This is test headline',
            'subject': [{'qcode': '04001000'}]
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'A'),
                         'This is test headline')

    def test_locator_for_categoryX_sport_topic(self):
        self.assertEqual(self.locator_map.map(self.article7, 'X'), 'SKI')

    def test_locator_for_categoryX_no_sport_topic(self):
        self.assertEqual(self.locator_map.map(self.article8, 'X'), 'CHN')

    def test_headline_prefix_not_for_racing(self):
        article = {
            '_id': 'urn:newsml:localhost:2018-07-19T15:25:10.511062:feabfc1d-7686-4d39-bc88-b91fc2bd5b1e',
            'source': 'BRA',
            'headline': 'Townsville gallops selections Saturday',
            'anpa_category': [
                {
                    'qcode': 'r',
                    'name': 'Racing (Turf)'
                }
            ],
            'type': 'text',
            'subject': [

                {
                    'qcode': '15030000',
                    'name': 'horse racing, harness racing'
                }
            ],
            'body_html': '<pre>Townsville gallops selections Saturday</pre>'
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'R'),
                         'Townsville gallops selections Saturday')

    def test_headline_prefix_missing_sport(self):
        article = {
            'headline': 'This is test headline',
            'subject': [{'qcode': '15073000'}],
            'place': [{
                'name': 'NSW',
                'state': '',
                'world_region': 'Oceania',
                'group': 'Australia',
                'qcode': 'NSW',
                'country': 'Australia'
            }]
        }

        self.assertEqual(self.locator_map.get_formatted_headline(article, 'S'),
                         'SPO:This is test headline')
