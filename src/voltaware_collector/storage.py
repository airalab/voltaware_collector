# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from . import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/storage.db'
db = SQLAlchemy(app)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumption = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)

    def __repr__(self):
        return '<Sensor(id={}, consumption={}, last_update={})>'.format(
                self.id, self.consumption, self.last_update)

class Offset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumption = db.Column(db.Integer)
    stamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Offset(id={}, consumption={} stamp={})>'.format(
                self.id, self.consumption, self.stamp)

db.create_all()

@app.route('/measurement/<int:sensor_id>/<int:consumption>/<stamp>', methods=['PUT'])
def put_measurement(sensor_id, consumption, stamp):
    '''
        Put sensor measurement by sensor id.
    '''
    sensor = Sensor.query.get(sensor_id)
    if sensor:
        sensor.consumption = consumption 
        sensor.last_update = stamp 
    else:
        db.session.add(Sensor(id=sensor_id, consumption=consumption, last_update=stamp)) 
    db.session.commit()
    return 'success'

@app.route('/offset/<int:consumption>/<int:stamp>', methods=['PUT'])
def put_offset(consumption, stamp):
    '''
        Put carbon offsetting.
    '''
    db.session.add(Offset(consumption=consumption, stamp=datetime.fromtimestamp(stamp)))
    db.session.commit()
    return 'success'

@app.route('/total_consumption')
def total_consumption():
    '''
        Returns offsetted energy consumption.
    '''
    offset = sum([x.consumption for x in Offset.query.all()])
    consumption = sum([x.consumption for x in Sensor.query.all()])
    return str(consumption - offset)
