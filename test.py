#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from pgjson.mapping import PgDocument, Mapping, ListField, \
    TextField, BooleanField, DictField
from pgjson.client import PgDatabase


class User(PgDocument):
    _version = 1

    profile = DictField(Mapping.build(
        profile_text=TextField(),
        language=TextField(),
        profile_image_url=TextField(),
        timezone=TextField(),
        phone=TextField(),
        location=TextField(),
        urls=ListField(DictField(Mapping.build(
            url=TextField(),
            description=TextField(),
            label=TextField(),
        ))),
        callname=TextField(),
        biz_address=TextField(),
        fullname=TextField(),
    ))
    locked = BooleanField(default=False)
    email = TextField()


class Entry(PgDocument):
    _table = 'entries'
    _version = 1

    name = TextField()


db = PgDatabase("postgres://joni@localhost/test")
db.setup_tables()

user = User(email='blah@example.org')
user.profile.callname = u'John Doe'
user.store(db)
print user
