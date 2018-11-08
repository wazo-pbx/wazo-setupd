# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import (
    all_of,
    assert_that,
    calling,
    has_property,
)
from xivo_test_helpers.hamcrest.raises import raises

from .helpers.base import BaseIntegrationTest
from .helpers.base import VALID_TOKEN
from .helpers.wait_strategy import NoWaitStrategy

from wazo_setupd_client.exceptions import SetupdError


class TestConfig(BaseIntegrationTest):

    asset = 'base'
    wait_strategy = NoWaitStrategy()

    def test_setup_empty(self):
        setupd = self.make_setupd(VALID_TOKEN)

        assert_that(calling(setupd.setup.create).with_args({}),
                    raises(SetupdError).matching(has_property('status_code', 400)))

    def test_setup_invalid_credentials(self):
        setupd = self.make_setupd(VALID_TOKEN)
        body = {
            'engine_entity_name': 'Wazo',
            'engine_language': 'en_US',
            'engine_number_start': '1000',
            'engine_number_end': '1999',
            'engine_password': 'secret',
            'nestbox_host': 'nestbox-auth',
            'nestbox_port': 9497,
            'nestbox_verify_certificate': False,
            'nestbox_service_id': 'test',
            'nestbox_service_key': 'foobar',
            'nestbox_instance_name': 'my-wazo',
            'nestbox_engine_host': 'wazo.example.com',
            'nestbox_engine_port': 443,
        }

        assert_that(calling(setupd.setup.create).with_args(body),
                    raises(SetupdError).matching(all_of(has_property('status_code', 500),
                                                        has_property('error_id', 'setup-token-failed'))))

    def test_setup_valid(self):
        setupd = self.make_setupd(VALID_TOKEN)
        body = {
            'engine_entity_name': 'Wazo',
            'engine_language': 'en_US',
            'engine_number_start': '1000',
            'engine_number_end': '1999',
            'engine_password': 'secret',
            'nestbox_host': 'nestbox.example.com',
            'nestbox_port': 443,
            'nestbox_service_id': 'nestbox-user',
            'nestbox_service_key': 'secret',
            'nestbox_instance_name': 'my-wazo',
            'nestbox_engine_host': 'wazo.example.com',
            'nestbox_engine_port': 443,
        }

        setupd.setup.create(body)
