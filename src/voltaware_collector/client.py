# -*- coding: utf-8 -*-

from datetime import datetime
from json import loads
import pika, rospy

from . import app 
from . import storage

class VoltawareClient:
    def __init__(self):
        rospy.loginfo('Initialize Voltaware client...')

        login = rospy.get_param('~login')
        password = rospy.get_param('~password')
        host = rospy.get_param('~host')
        self.queue_name = rospy.get_param('~queue')

        credentials = pika.PlainCredentials(login, password)
        params = pika.ConnectionParameters(host=host, port=5672, virtual_host='/', heartbeat=60, credentials=credentials)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=10)

        rospy.loginfo('Voltaware client initialized')

    def run(self):
        def write_measurement(ch, method, properties, body):
            '''
                Write Voltaware sensor measurements.
            '''
            json = loads(body)
            sensor_id = json['sensor']['id']
            consumption = json['event']['energyConsumptionWh']
            stamp = datetime.strptime(json['event']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            rospy.loginfo('Incoming measurement from {} at {}, consumption {} Wh'.format(sensor_id, stamp, consumption))
            storage.put_measurement(sensor_id, consumption, stamp)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(self.queue_name, write_measurement)
        self.channel.start_consuming()

    def close(self):
        self.channel.stop_consuming()
        self.connection.close()
