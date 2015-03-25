#! /usr/bin/env python
# -8- coding: utf-8 -*-

session_config = {
    'auto_session_enable': True,
    'session_permanent': False,
    'secret_key': 'jwfy_gdesion_propject_2015_03_25',
    'session_engine': 'redis',
    'session_key_function': None,
    'session_cookie_name': 'jwfy_session',
    'session_cookie_age': 60*60*24*2,
    'session_cookie_domain': '127.0.0.1',
    'session_cookie_secure': False,
    'session_cookie_path': '/',
    'session_save_every_request': True,
    'session_expire_at_browser_close': False,
    session_db_config: {
        'db': 15,
        'host':'127.0.0.1',
        'port':6380
        }
}
