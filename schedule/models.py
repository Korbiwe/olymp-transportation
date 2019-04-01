from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from core.models import db, BaseModel

routes_stops = db.Table(
    'routes_stops',
    db.Column('route_id', db.Integer(), db.ForeignKey('stop.id')),
    db.Column('stop_id', db.Integer(), db.ForeignKey('route.id'))
)


class Park(BaseModel):
    __tablename__ = 'park'
    name = db.Column(db.String(255))
    locationLong = db.Column(db.Float(precision=64), nullable=False)
    locationLat = db.Column(db.Float(precision=64), nullable=False)

    vehicles = relationship('Vehicle')

    def __repr__(self):
        return self.name


class VehicleType(BaseModel):
    __tablename__ = 'vehicle_type'
    name = db.Column(db.String(255), unique=True)

    vehicles = relationship('Vehicle')
    drivers = relationship('Driver')

    def __repr__(self):
        return self.name


class Vehicle(BaseModel):
    __tablename__ = 'vehicle'
    factoryNum = db.Column(db.String(255), unique=True)
    year = db.Column(db.Integer(), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    manufacturedBy = db.Column(db.String(255), nullable=False)

    type_id = db.Column(db.Integer, ForeignKey('vehicle_type.id'), nullable=False)
    type = relationship('VehicleType')
    park_id = db.Column(db.Integer, ForeignKey('park.id'), nullable=False)
    park = relationship('Park')

    entries = relationship('ScheduleEntry')

    __table_args__ = (CheckConstraint(f'1900 < year < {datetime.now().year}', name='is_year_valid_check'), {})

    def __repr__(self):
        return f'{self.model} номер {self.factoryNum} ({self.year} года)'


class Driver(BaseModel):
    __tablename__ = 'driver'
    fullName = db.Column(db.String(255), nullable=False)
    licenseNum = db.Column(db.String(255), unique=True, nullable=False)

    type_id = db.Column(db.Integer, ForeignKey('vehicle_type.id'), nullable=False)
    type = relationship('VehicleType')
    entries = relationship('ScheduleEntry')

    def __repr__(self):
        return self.fullName


class Route(BaseModel):
    __tablename__ = 'route'
    name = db.Column(db.String(255))
    distanceKm = db.Column(db.Integer)

    entries = relationship('ScheduleEntry')
    stops = relationship(
        'Stop',
        secondary=routes_stops,
        back_populates='routes'
    )

    __table_args__ = (CheckConstraint('distanceKm > 0', name='is_distance_positive_check'), {})

    def __repr__(self):
        return self.name


class Stop(BaseModel):
    __tablename__ = 'stop'
    name = db.Column(db.String(255), nullable=False)
    locationLong = db.Column(db.Float(precision=64), nullable=False)
    locationLat = db.Column(db.Float(precision=64), nullable=False)

    routes = relationship(
        'Route',
        secondary=routes_stops,
        back_populates='stops'
    )

    def __repr__(self):
        return self.name


class ScheduleEntry(BaseModel):
    __tablename__ = 'schedule_entry'
    name = db.Column(db.String(255))

    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)

    driver_id = db.Column(db.Integer, ForeignKey('driver.id'), nullable=False)
    driver = relationship('Driver', back_populates='entries')
    route_id = db.Column(db.Integer, ForeignKey('route.id'), nullable=False)
    route = relationship('Route', back_populates='entries')
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.id'), nullable=False)
    vehicle = relationship('Vehicle', back_populates='entries')

    def __repr__(self):
        return f'{self.name}({self.id})'

