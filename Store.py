#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import json
from DataBag import *
from httplib import HTTPConnection
from base64 import b64encode

servers = None

def getSchoolData(host='', url='/', method='GET', body='', user='', password=''):
    """
    Gather school data from halley
    """
    connection = HTTPConnection(host)
    if (connection):
        try:
            header = {}
            auth = b64encode(b"%s:%s" % (user, password))
            header = {"Content-Type": 'application/json',
                        "Accept":"text/plain",
                        "Authorization": 'Basic %s' % auth}
            connection.request(method, url, body, header)
            response = connection.getresponse()
            data = response.read()
            connection.close()
            return data
        except Exception, e:
            raise Exception("Can't get information %s " % str(e))
        finally:
            if (connection):
                connection.close()

def makeData(addr):
    global servers
    data = getSchoolData(host="example.com", body='{"ip":"%s"}' % addr, user="example", password="secret")
    try:
        data = json.loads(data)
        servers.setData(addr, data)
    except Exception as err:
        pass

servers = DataBag()
servers.deserialize("store.db")
makedata("192.168.0.100")
servers.serialize("store.db")

