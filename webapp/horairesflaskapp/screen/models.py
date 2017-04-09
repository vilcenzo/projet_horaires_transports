# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from horairesflaskapp.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Screen(SurrogatePK, Model):
    """Board of a user"""

    __tablename__ = 'screens'
    gare_depart = Column(db.Integer(), unique=False, nullable=False)
    gare_arrive = Column(db.Integer(), unique=False, nullable=False)
    titre_affichage = Column(db.String(18), unique=False, nullable=False)
    type_transport = Column(db.String(10), unique=False, nullable=False)
    board_id = reference_col('boards', nullable=False)
    board = relationship('Board', backref='screens')

    def __init__(self, board_id, gare_depart, gare_arrive, titre_affichage, type_transport, **kwargs):
        """Create instance."""
        db.Model.__init__(self, board_id=board_id, gare_depart=gare_depart,
                          gare_arrive=gare_arrive, titre_affichage = titre_affichage,
                          type_transport = type_transport,  **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Screen({id})>'.format(id=self.board_id)