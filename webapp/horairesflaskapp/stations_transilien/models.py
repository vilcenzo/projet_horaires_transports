# -*- coding: utf-8 -*-

from horairesflaskapp.database import Column, Model, SurrogatePK, db


class StationTransilien(SurrogatePK, Model):
    """Station de transilien"""

    __tablename__ = 'stations_transiliens'
    name = Column(db.String(80), unique=True, nullable=False)
    uic = Column(db.Integer(), unique=False, nullable=False)

    def __init__(self, name, uic, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, uic=uic, **kwargs)

    def __repr__(self):
        return 'Station {name} uic {uic} '.format(name=self.name, uic=self.uic)
