# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.auth_verifier import required_acl

from wazo_setupd.http import AuthResource


class ConfigResource(AuthResource):
    def __init__(self, config):
        self._config = config

    @required_acl('setupd.config.read')
    def get(self):
        return dict(self._config), 200
