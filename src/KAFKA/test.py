from confluent_kafka import Producer
from confluent_kafka import Consumer
conf = {'bootstrap.servers':"pkc-6ojv2.us-west4.gcp.confluent.cloud:9092",
        'security.protocol':'SASL_SSL',
        'sasl.mechanisms':'PLAIN',
        'sasl.username':'AMD3FYNELYF4W6FB',
        'sasl.password':'OcUpeg7LE+26okMZJzCCLK319i7cDwJKDX8mw21BubKm70GU9XFRPI829mfI42eI',
          }


producer = Producer(conf)
producer.produce("notification", key="key", value="value")

props = conf
props["group.id"] = "test"
props["auto.offset.reset"] = "earliest"

consumer = Consumer(props)
consumer.subscribe(["notification"])
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            print("key = {key:12} value = {value:12}".format(key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
except KeyboardInterrupt:
    pass
finally:
         consumer.close()