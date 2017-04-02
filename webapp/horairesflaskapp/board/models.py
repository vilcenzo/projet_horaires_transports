# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from horairesflaskapp.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Board(SurrogatePK, Model):
    """Board of a user"""

    __tablename__ = 'boards'
    name = Column(db.String(80), nullable=False)
    chip_id = Column(db.String(80), nullable=False, unique=True)
    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='boards')

    def __init__(self, name, chip_id, user_id, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, chip_id=chip_id, user_id=user_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Board({name})>".format(name=self.name)
