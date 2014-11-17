#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from postgres import Postgres
from pgjson.mapping import PgDocument


class PgDatabase(Postgres):
    def __init__(self, url):
        Postgres.__init__(self, url)

    def delete(self, doc):
        """
        True if deleted, False otherwise (object did not exist)
        """
        if doc.id is None:
            raise Exception('Cannot delete object with id=None')
        with self.get_cursor() as cursor:
            cursor.run("DELETE FROM %s " % doc._table +
                       "WHERE id=%s;", [doc.id])
            return cursor.rowcount > 0

    def setup_tables(self):
        for cls in PgDocument.__subclasses__():
            cls.__call__().setup_table(self)
