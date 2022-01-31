class Dao:
    def __init__(self, db):
        self.db = db

    def init_app(self, app):
        self.db.init_app(app)

    def add(self, record):
        self.db.add(record)
        self.db.commit()

    def delete(self, record):
        self.db.delete(record)
        self.db.commit()
