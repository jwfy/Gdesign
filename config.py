#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author:jwfy
# time:2015-03-25
# e-mail:jwfy0902@foxmail.com

import sys
import os
import logging
import sputnik.SpuConfig as SpuConfig
from sputnik.Sputnik import set_logging_config
from tornado.options import define, options, parse_command_line, enable_pretty_logging
from sputnik.SpuLogging import *

config_file = sys.argv[-1]
dirname, basename = os.path.split(config_file)
module_name = basename.split(".")[0]
sys.path.append(dirname)
cm = __import__(module_name)

define("server_port", default=None, help="run on the given server port", type=int)
define("app_port", default=None, help="run on the given application port", type=int)
define("debug", default=None, help="debug", type=bool)
parse_command_line()

DEBUG = options.debug or cm.debug
app_port = options.app_port

debug_logging_config = {
    'log_slow': True,
    'log_slow_time': 500,
    'flowpath_db_detail': True,
    'flowpath_cache_detail': True,
    'log_function': {
        'all': False,
        'flowpath':{
            'all': False,
            'flowpath': False,
            'logic': False,
            'service': False,
            'db': True,
            'cache': True
        },
        'perf':{
            'all': False,
            'perf': False,
            'func': False,
            'service': False,
            'db': True,
            'cache': True
        }
    }
}

# mogodb config
mongo_dbcnf = {
    'host' : cm.mongo_db_host, 
    'port' : cm.mongo_db_port,
    'database' : cm.mongo_db_database,
    'user' : cm.mongo_db_user,
    'passwd' : cm.mongo_db_password,
    'debug' : DEBUG
    }

app_port = options.app_port

spusys_config = {
    'enable': True,
    'spumaster_server_addr': cm.SPUMASTER_ADDRESS,
    'app_port': app_port,
    'http_thread': False,
    'network_interface': cm.LOCAL_ADDRESS,
    }
from sputnik import sputnik_init
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)
sputnik_init(debug_logging_config, spusys_config=spusys_config)

from sputnik.SpuFieldFilter import SpuFieldFilter
from sputnik.SpuDB import SpuDB_Tornado
SpuConfig.SpuSession_Config = cm.session_config
session_config = cm.session_config

SpuConfig.SpuDebug = DEBUG
SpuFieldFilter.debug = DEBUG
version = 0.1
run_mode = cm.run_mode

start_sputnik_logging(error_log_path=cm.ERROR_LOG_PATH)

mysql_dbcnf = {
    'dbtype' : SpuDB_Tornado, 
    'host': cm.mysql_db_host,
    'port':cm.mysql_db_port,
    'database': cm.mysql_db_database,
    'user': cm.mysql_db_user,
    'passwd': cm.mysql_db_password,
    'debug': DEBUG
    }

