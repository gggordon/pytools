#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2015-11-03 21:38:52 +0000 (Tue, 03 Nov 2015)
#
#  https://github.com/harisekhon/pytools
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback to help improve or steer this or other code I publish
#
#  http://www.linkedin.com/in/harisekhon
#

"""

HiveServer2 Tester

Can inherit HiveTester class to other programs and override the execute() method with arbitrary SQL statements to execute

"""

from __future__ import print_function

__author__  = 'Hari Sekhon'
__version__ = '0.1'

import glob
import logging
import os
import sys
# using optparse rather than argparse for servers still on Python 2.6
from optparse import OptionParser
try:
    import pyhs2
except ImportError, e:
    print('failed to import pyhs2: %s (see installation instructions at https://github.com/harisekhon/pytools)' % e)
    sys.exit(4)
sys.path.append(os.path.join(os.path.dirname(__file__), 'pylib'))
try:
    from harisekhon.utils import *
    from harisekhon import CLI
except ImportError, e:
    print('module import failed: %s' % e, file=sys.stderr)
    sys.exit(4)


class HiveServer2Tester(CLI):

    def add_options(self):
        self.add_hostoption('Hive', default_host='localhost', default_port=10000)
        self.add_useroption('Hive')
        self.parser.add_option('-f', '--sql-files', dest='sqlFiles', help='Hive SQL files to execute',
                          metavar='file1.sql,file2.sql', action='append')
        db_envs, default_db = getenvs2('DATABASE', 'default', name='Hive')
        self.parser.add_option('-d', '--database', dest='database', help="Hive Database to connect to (%s)" % db_envs,
                          metavar='database', default=default_db)
        self.parser.add_option('-k', '--kerberos', dest='kerberos', help='Kerberos authentication', action='store_true')

    def run(self):
        log = logging.getLogger(prog)
        log.setLevel(logging.INFO)

        if self.args or not self.options.sqlFiles:
            self.usage()

        try:
            validate_host(self.options.host)
            validate_port(self.options.port)
            # TODO: XXX: user is not set despite $USER in env
            validate_user(self.options.user)
            validate_password(self.options.password)
        except InvalidOptionException, e:
            die(e)

        self.authMechanism = 'PLAIN'
        if self.options.kerberos:
            self.authMechanism = 'KERBEROS'

        # TODO: XXX: copy this to an impala program using impyla
        # switch this program to use impyla as pyhs2 has all sorts of exceptions around connect when user isn't specified
        # with kerberos: thrift.transport.TTransport.TTransportException: Bad status: 3 (Problem with callback handler)

        self.connect()
        self.execute()

    def connect(self, database='default'):
        self.conn = pyhs2.connect(host=self.options.host,
                                  port=self.options.port,
                                  authMechanism=self.authMechanism,
                                  user=self.options.user,
                                  password=self.options.password,
                                  database=database)
        self.cur = self.conn.cursor()

    def execute(self):
        #Show databases
        print(self.cur.getDatabases())

        #Execute query
        self.cur.execute("select * from cars")

        #Return column info from query
        print(self.cur.getSchema())

        #Fetch table results
        for i in self.cur.fetch():
            print(i)


if __name__ == '__main__':
    HiveServer2Tester().main()
