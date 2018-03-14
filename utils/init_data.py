#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/18 9:46 AM
# @Author  : Miracle Young
# @File    : init_data.py

import pymysql, uuid, datetime, platform

conn_str = {
    'host': '127.0.0.1' if 'linux' in platform.platform().lower() else '172.16.46.182',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'MiracleOps',
    'charset': 'utf8mb4'
}

conn = pymysql.connect(**conn_str)
with conn.cursor() as cursor:
    print('role init starting...')
    init_role_sql = '''
        insert into role (`name`, `c_time`) values ('{}', '{}');
        insert into role (`name`, `c_time`) values ('{}', '{}');
        insert into role (`name`, `c_time`) values ('{}', '{}');
        insert into role (`name`, `c_time`) values ('{}', '{}');
    '''.format('Anonymous', datetime.datetime.now(), 'Normal', datetime.datetime.now(), 'Admin',
               datetime.datetime.now(), 'UnVerified', datetime.datetime.now())
    cursor.execute(init_role_sql)

    init_job_sql = '''
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
        insert into job (`id`, `name`, `c_time`) values ({}, '{}', now());
    '''.format(-1, 'Undefined', 1, 'Database Administrator', 2, 'System Administrator', 3, 'Network Administrator', 4,
               'Help Desk/IT', 5, 'Developer', 6, 'Tester', 101, 'Director', 102, 'Manager', 103, 'Tech Leader')
    cursor.execute(init_job_sql)
    conn.commit()
    print('role init completed.')
    conn.close()
