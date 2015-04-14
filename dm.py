#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import *
from sputnik.SpuUOM import SpuUOM
from sputnik.SpuFS import *
from sputnik.SpuDebug import *
from sputnik.SpuFactory import *
from sputnik.SpuRequest import set_auto_session_engine
from sputnik.SpuDB import SpuDBCreateDB, SpuMongodb
from sputnik.SpuContext import SpuContext
import sys
sys.path.insert(0, 'api')

def init():

    SpuUOM.import_module('user')
    SpuUOM.import_module('movie')
    SpuUOM.load()
   
    mongodb = SpuMongodb(mongo_dbcnf)
    mongodb.connection()
    SpuContext.init_context(None, mongodb)

    mysql_db = SpuDBCreateDB(mysql_dbcnf)
    mysql_dbc = mysql_db.create() 
    mysql_dbc.set_charset('utf8mb4')
    mysql_dbc.connection() 
    SpuContext.init_context(mysql_dbc, None)
    
    SpuDBManager.add_spudb(mysql_dbc) 
    SpuDOFactory.init_factory(True)  

def start():
    class Application(tornado.web.Application):
        def __init__(self):
            if DEBUG:
                doc = True
            else:
                doc = False
            handlers = SpuUOM.url_rule_list(doc)
            settings = dict(
                service_title=u"Web Site",
                template_path=os.path.join(os.path.dirname(__file__), "templates"), 
                static_path=os.path.join(os.path.dirname(__file__), "static")
                )
            tornado.web.Application.__init__(self, handlers, debug=DEBUG, **settings)

    http_server = tornado.httpserver.HTTPServer(Application(), xheaders = True)
    SpuLogging.info("start success")
    http_server.listen(app_port)
    tornado.ioloop.IOLoop.instance().start()


def print_db_info():
    SpuLogging.info("DB Info:")
    SpuLogging.info("\tDB Type:%s" % DBCNF['dbtype'])
    SpuLogging.info("\tDB Host:%s" % DBCNF['host'])
    SpuLogging.info("\tDB Port:%s" % DBCNF['port'])
    SpuLogging.info("\tDB Database:%s" % DBCNF['database'])

def print_sys_info():
    SpuLogging.info("Tornado Version: %s" % tornado.version)
    SpuLogging.info("Application Port:%s" % app_port)
    SpuLogging.info("Debug Mod:%s" % DEBUG)

def usage():
    print "usage: ./dm.py [--option=value] configfile [--dev]"
    print "\t --dev\t\tno install Module"

def main():
    init()
    print_sys_info()
    start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    main()
