#!/usr/bin/python

import csv, ldap, ConfigParser, MySQLdb, time, sys, os

cfg = ConfigParser.ConfigParser()
cfg.read('/opt/usermanager/etc/usermanager.ini')

dbuser = cfg.get('database', 'user')
dbpass = cfg.get('database', 'passwd')
dbname = cfg.get('database', 'db')
dbhost = cfg.get('database', 'host')
audit = cfg.getboolean('logging', 'audit')
debug = cfg.getboolean('logging', 'debug')
audit_log_file = cfg.get('logging', 'auditlog')
debug_log_file = cfg.get('logging', 'debuglog')

private_ldap_host = cfg.get('privateldap', 'host')

private_ldap_user_basedn = cfg.get('privateldap', 'user_basedn')
private_ldap_group_basedn = cfg.get('privateldap', 'group_basedn')

private_ldap_adminuser = cfg.get('privateldap', 'adminuser')
private_ldap_adminpass = cfg.get('privateldap', 'adminpass')

campus_ldap_host = cfg.get('campusldap', 'host')
campus_ldap_basedn = cfg.get('campusldap', 'basedn')

if debug:
    debuglog = open(debug_log_file, 'a+')

if audit:
    auditlog = open(audit_log_file, 'a+')

# Connect to the database
db = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpass,db=dbname)

requestor = 'alextsoi'

curs = db.cursor()
query = 'SELECT COUNT(*) FROM users where uniqname = \'' + requestor + '\';'
curs.execute(query)
report = curs.fetchone()
countup = report[0]

if countup == 0:
    requestormail = requestor + '@umich.edu'
else:
    curs = db.cursor()
    query = 'SELECT emailaddress FROM users where uniqname = \'' + requestor + '\';'
    curs.execute(query)
    report = curs.fetchone()
    requestormail = report[0]

print(requestormail)

