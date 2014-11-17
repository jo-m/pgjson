#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from couchdb.mapping import Document, Mapping, TextField, \
    DateTimeField, BooleanField, FloatField, ListField, \
    DictField, IntegerField, LongField
import json
import inflect
import psycopg2

_inflect = inflect.engine()


class PgDocument(Document):
    _table = None
    _version = None

    __deleted = False

    def __init__(self, id=None, **values):
        super(PgDocument, self).__init__(id, **values)
        if id is not None:
            self.id = id

        self._table = self.__class__.get_table()
        self.type = self.__class__.__name__.lower()
        self._data['type'] = self.type

        if self._version is None:
            raise Exception('_version must be set!')

    def store(self, db):
        try:
            if self.id is None:
                self.__create(db)
            else:
                self.__update(db)
            return self
        except psycopg2.ProgrammingError:
            raise Exception('Table %s does not exist!' % self._table)

    def setup_table(self, db):
        db.run("CREATE TABLE IF NOT EXISTS %s " % self._table +
               "(id SERIAL, version INT, doc JSON);")

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

    def delete(self, db):
        db.delete(self)
        del self._data['_id']
        self.__deleted = True

    def __getitem__(self, name):
        """
        doc = db[doc_id]
        """
        pass

    def json(self):
        return json.dumps(self._data)

    @classmethod
    def get_table(cls):
        if cls._table is None:
            return _inflect.plural(cls.__name__).lower()
        return cls._table

    @classmethod
    def load(cls, db, id):
        table = cls.get_table()
        rec = db.one("SELECT * FROM %s " % table +
                     "WHERE id=%s", [id])
        obj = cls.wrap(rec.doc)
        obj.id = rec.id
        return obj

    def __repr__(self):
        return '<%s %r@%s %r>' % (type(self).__name__, self.id, self._table,
                                  dict([(k, v) for k, v in self.items()
                                        if k not in ('_id')]))


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
