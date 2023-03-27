from kafka import KafkaConsumer

bootstrap_servers = ['pkc-03vj5.europe-west8.gcp.confluent.cloud:9092']
topicName = 'meteo1'
consumer_group = 'your_consumer_group_id'

consumer = KafkaConsumer(topicName, group_id=consumer_group, bootstrap_servers = bootstrap_servers,
                         security_protocol='SASL_SSL', sasl_mechanism='PLAIN',
                         sasl_plain_username='EEVMZ6X54FESIITW',
                         sasl_plain_password='SoeBfjdTAm/MhA06GQzm5B77+1c2+RLlymtwtohuSaRXXIhDAF55NGT3Ejj9ukG/')

for message in consumer:
    print("hehexd")
    print(message.value)