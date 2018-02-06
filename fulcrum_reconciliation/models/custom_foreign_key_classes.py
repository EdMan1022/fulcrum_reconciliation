from sqlalchemy import ForeignKey


class ForeignKeyCascade(ForeignKey):
    def __init__(self, column, **dialect_kw):
        super().__init__(column, **dialect_kw)
        self.onupdate = "CASCADE"
        self.ondelete = "CASCADE"
        self.index = True


class ForeignKeyNull(ForeignKey):
    def __init__(self, column, **dialect_kw):
        super().__init__(column, **dialect_kw)
        self.onupdate = "CASCADE"
        self.ondelete = "SET NULL"
        self.index = True