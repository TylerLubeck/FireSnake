# -*- coding: utf-8 -*-
# typing imports
from typing import Optional, Dict  # noqa
# end typing imports

import requests

from firesnake.validators import (
    validate_fcm_package,
)

__all__ = ('FCM',)

FCM_URL = 'https://fcm.googleapis.com/fcm/send'

def FCM(object):
    def __init__(self, fcm_key, headers=None):
        # type: (str, Optional[Dict[str,str]]) -> None
        self.__fcm_key = fcm_key
        self.headers = {
            'Authorization': 'key={}'.format(fcm_key),
            'Content-Type': 'application/json',
        }
        if headers is not None:
            self.headers.update(headers)

    def
