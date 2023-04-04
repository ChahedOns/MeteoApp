import json
from flask import make_response
from app import Notification
from configparser import ConfigParser
from confluent_kafka import Producer, Consumer


producer_config = {'bootstrap.servers':"pkc-6ojv2.us-west4.gcp.confluent.cloud:9092",
        'security.protocol':'SASL_SSL',
        'sasl.mechanisms':'PLAIN',
        'sasl.username':'AMD3FYNELYF4W6FB',
        'sasl.password':'OcUpeg7LE+26okMZJzCCLK319i7cDwJKDX8mw21BubKm70GU9XFRPI829mfI42eI'
          }
consumer_config = {'bootstrap.servers':"pkc-6ojv2.us-west4.gcp.confluent.cloud:9092",
        'security.protocol':'SASL_SSL',
        'sasl.mechanisms':'PLAIN',
        'sasl.username':'AMD3FYNELYF4W6FB',
        'sasl.password':'OcUpeg7LE+26okMZJzCCLK319i7cDwJKDX8mw21BubKm70GU9XFRPI829mfI42eI',
        'auto.offset.reset':'earliest',
        'group.id':'notification',
        'enable.auto.commit':'true',
        'max.poll.interval.ms':'3000000',}
notif_producer = Producer(producer_config)


def load_notif(msg,id):
    notif_consumer = Consumer(consumer_config)
    notif_consumer.subscribe(['notification'])
    while True:
        event =notif_consumer.poll(1.0)
        if event is None:
            pass
        elif event.error():
            print(f'Bummer - {event.error()}')
        else:
            notif = json.loads(event.value())
            add_notif(msg)

def add_notif(msg):
    n = Notification(id=id,msg=msg)
    return make_response("Notification sent!",200)