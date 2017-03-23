# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from horairesflaskapp.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Screen(SurrogatePK, Model):
    """Board of a user"""

    __tablename__ = 'screens'
    gare_depart = Column(db.Integer(), unique=False, nullable=False)
    gare_arrive = Column(db.Integer(), unique=False, nullable=False)
    board_id = reference_col('boards', nullable=False)
    board = relationship('Board', backref='screens')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Screen({id})>'.format(id=self.board_id)