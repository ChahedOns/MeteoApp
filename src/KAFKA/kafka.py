from confluent_kafka.admin import AdminClient , NewTopic
from confluent_kafka import Producer
conf = {'bootstrap.servers':"pkc-6ojv2.us-west4.gcp.confluent.cloud:9092",
        'security.protocol':'SASL_SSL',
        'sasl.mechanisms':'PLAIN',
        'sasl.username':'AMD3FYNELYF4W6FB',
        'sasl.password':'OcUpeg7LE+26okMZJzCCLK319i7cDwJKDX8mw21BubKm70GU9XFRPI829mfI42eI'
          }
ac=AdminClient(conf)
topic=NewTopic('notifications',num_partitions=6,replication_factor=1)
fs=ac.create_topics([topic])

producer = Producer(conf)

data = "sending data =>"
arr=[1,2,3,4,5,6,7]

for x in arr:
    producer.produce('notifications',data.encode('utf-8'),callback= lambda err,msg : print("message deleveried to topic => 11", msg.topic(),"@ partition : ", msg.partition()))
producer.flush()