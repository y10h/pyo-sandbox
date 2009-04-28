#!/usr/bin/env python
# encoding: utf-8
"""
Move all data and schema from one database to another

Tool is created mostly for Django app migration from sqlite to mysql

Copyright 2009 Yury Yurevich
Licensed under terms of GNU GPL2
"""


import sqlalchemy as sa
import logging
import sys

_CACHED_TABLE_ORDER = []

def reflect_db(engine):
    meta = sa.MetaData()
    meta.bind = engine
    meta.reflect()
    return meta

def reorder_tables(meta):
    global _CACHED_TABLE_ORDER
    if _CACHED_TABLE_ORDER:
        return _CACHED_TABLE_ORDER
    dependencies = {}
    table_order = []
    all_tables = []
    tables = meta.tables
    for table in tables.values():
        all_tables.append(table.name)
        for fk in table.foreign_keys:
            remote_table_name = fk.column.table.name
            dependencies[table.name] = dependencies.get(table.name, []) + \
                                       [remote_table_name]
        # first, fill all tables without any dependencies
        if table.name not in dependencies and table.name not in table_order:
            table_order.append(table.name)

    unordered_tables = all_tables[:]
    i = 0
    while unordered_tables:
        i += 1
        if i > 1000*len(all_tables):
            short_deps = dict((u, dependencies[u]) for u in unordered_tables)
            logging.error('Infinite loop detected for data: unordered_tables=%s' % (unordered_tables,))
            logging.error('Infinite loop detected for data: unordered_tables depends on %s' % (short_deps,))
            logging.error('Infinite loop detected for data: already ordered tables are %s' % (table_order,))
            logging.error('Infinite loop detected for data: tables full dependencies are %s' % (dependencies,))
            raise RuntimeError('Infinite loop detected: cannot reorder tables %s' % (unordered_tables,))
        for t in all_tables:
            if t not in unordered_tables:
                continue
            if t in table_order:
                unordered_tables.remove(t)
                continue
            already_all_deps = True
            for dep in dependencies[t]:
                if dep not in table_order:
                    already_all_deps = False
            if already_all_deps:
                unordered_tables.remove(t)
                if t not in table_order:
                    table_order.append(t)

    _CACHED_TABLE_ORDER = [tables[k] for k in table_order]
    return _CACHED_TABLE_ORDER

def provide_schema(meta_from, meta_to):
    logging.info('syncing tables')
    for table in reorder_tables(meta_from):
        newtable = table.tometadata(meta_to)
        if newtable.exists():
            logging.debug('table %s already exists in target db' % newtable.name)
        else:
            logging.debug('creating table %s in target db' % newtable.name)
            newtable.create()

def flatten_record(rec):
    return dict((key, getattr(rec, key)) for key in rec.keys())

def move_data_by_table(table_from, table_to):
    conn_from = table_from.bind.connect()
    conn_to = table_to.bind.connect()
    query = sa.select([table_from])
    for rec in conn_from.execute(query).fetchall():
        data = flatten_record(rec)
        conn_to.execute(table_to.insert(values=data))
    conn_from.close()
    conn_to.close()

def clean_target(meta):
    logging.info('cleaning target db')
    conn = meta.bind.connect()
    for table in reversed(reorder_tables(meta)):
        logging.debug('cleaning data in table %s at target db' % table)
        conn.execute(table.delete())
    conn.close()

def move_data(meta_from, meta_to):
    logging.info('moving data')
    for table in reorder_tables(meta_from):
        logging.debug('moving data for table %s to target db' % table)
        newtable = table.tometadata(meta_to)
        move_data_by_table(table, newtable)

def move(from_db, to_db, clean_target_data=False):
    engine_from = sa.create_engine(from_db)
    logging.info('source db: %s' % engine_from)
    engine_to = sa.create_engine(to_db)
    logging.info('target db: %s' % engine_to)
    meta_from = reflect_db(engine_from)
    meta_to = reflect_db(engine_to)
    provide_schema(meta_from, meta_to)
    if clean_target_data:
        clean_target(meta_to)
    move_data(meta_from, meta_to)


def usage():
    print "movedb.py [--clean] <source-sqlalchemy-uri> <target-sqlalchemy-uri>"
    sys.exit(1)

def parse_args(args):
    if len(args) == 2:
        # without cleaning
        if args[0] == '--clean':
            usage()
        from_db = args[0]
        to_db = args[1]
        clean = False
    elif len(args) == 3:
        if args[0] != '--clean':
            usage()
        from_db = args[1]
        to_db = args[2]
        clean = True
    else:
        usage()
    return from_db, to_db, clean

def main(args):
    from_db, to_db, clean = parse_args(args)
    move(from_db, to_db, clean)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])

