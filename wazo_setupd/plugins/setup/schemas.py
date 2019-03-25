# -*- coding: utf-8 -*-
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from marshmallow import validates_schema
from marshmallow.exceptions import ValidationError
from xivo.mallow_helpers import Schema
from xivo.mallow import (
    fields,
    validate,
)


class SetupSchema(Schema):

    engine_language = fields.String(required=True, validate=validate.OneOf(['en_US', 'fr_FR']))
    engine_password = fields.String(required=True)
    engine_internal_address = fields.String(required=True)
    engine_license = fields.Boolean(required=True, validate=validate.Equal(True))
    nestbox_host = fields.String()
    nestbox_port = fields.Integer(
        validate=validate.Range(
            min=0,
            max=65535,
            error='Not a valid TCP/IP port number.'
        ),
        missing=443,
    )
    nestbox_verify_certificate = fields.Boolean(missing=True)
    nestbox_service_id = fields.String()
    nestbox_service_key = fields.String()
    nestbox_instance_name = fields.String()
    nestbox_engine_host = fields.String()
    nestbox_engine_port = fields.Integer(
        validate=validate.Range(
            min=0,
            max=65535,
            error='Not a valid TCP/IP port number.'
        ),
        missing=443,
    )

    @validates_schema
    def nestbox_all_or_nothing(self, data):
        if not data.get('nestbox_host'):
            return

        if 'nestbox_service_id' not in data:
            raise ValidationError('Missing keys for Nestbox configuration: nestbox_service_id')
        if 'nestbox_service_key' not in data:
            raise ValidationError('Missing keys for Nestbox configuration: nestbox_service_key')
        if 'nestbox_instance_name' not in data:
            raise ValidationError('Missing keys for Nestbox configuration: nestbox_instance_name')
        if 'nestbox_engine_host' not in data:
            raise ValidationError('Missing keys for Nestbox configuration: nestbox_engine_host')


setup_schema = SetupSchema()
