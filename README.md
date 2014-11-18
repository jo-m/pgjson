# PgJSON
A highly experimental, extremely hacky but working attempt to mis-use PostgreSQL as a document oriented database.

Much is inspired and stolen from [CouchDB-Python](https://github.com/djc/couchdb-python), especially the [Mappings](https://pythonhosted.org/CouchDB/mapping.html).

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
    
    db = PgDatabase("postgres://localhost/test")
    db.setup_tables()
    
    user = User(email='john@example.org')
    user.profile.callname = u'John Doe'
    user.store(db)
    print user.id
