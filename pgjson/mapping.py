#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from couchdb.mapping import Document, Mapping, TextField, \
    DateTimeField, BooleanField, FloatField, ListField, \
    DictField, IntegerField, LongField
import json
import inflect

_inflect = inflect.engine()


class PgDocument(Document):
    _table = None
    _version = None
    # id = LongField()

    def __init__(self, id=None, **values):
        super(PgDocument, self).__init__(id, **values)
        if id is not None:
            self.id = id

        if self._table is None:
            self._table = _inflect.plural(self.__class__.__name__).lower()

        if self._version is None:
            raise Exception('_version must be set!')

    def store(self, db):
        if self.__id is None and self.id is None:
            self.__create(db)
        else:
            self.__update(db)
        return self

    def __create(self, db):
        json_data = json.dumps(self._data)
        self.id = db.one("INSERT INTO %s " % self._table +
                         "(version, doc) VALUES (%s, %s) RETURNING id",
                         (self._version, json_data))
        return self.id

    def __update(self, db):
        json_data = json.dumps(self._data)
        with db.get_cursor() as cursor:
            cursor.run("UPDATE %s SET " % self._table +
                       "doc=%s WHERE id=%s;", (json_data, self.id))
            if cursor.rowcount != 1:
                raise Exception('Document not found (id=%s, table=%s)'
                                % (str(self.id), self._table))

    @classmethod
    def load(cls, db, id):
        # doc = db.get(id)
        # if doc is None:
        #     return None
        # return cls.wrap(doc)
        pass


class Mapping(Mapping):
    pass


class TextField(TextField):
    pass


class DateTimeField(DateTimeField):
    pass


class BooleanField(BooleanField):
    pass


class FloatField(FloatField):
    pass


class ListField(ListField):
    pass


class DictField(DictField):
    pass


class IntegerField(IntegerField):
    pass


class LongField(LongField):
    pass
