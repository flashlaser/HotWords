# coding=utf-8

import sys
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__=='__main__':
    kafkaHost='127.0.0.1'
    kafkaPort=9092
    kafkaTopic='hello kafka'

    ## 生产者
    producer=KafkaProducer(bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
        kafka_host=kafkaHost,
        kafka_port=kafkaPort
    )])

    messageStr='some message'
    producer.send(kafkaTopic, messageStr.encode('utf-8'))

    ##　消费者
    consumer=KafkaConsumer(
        kafkaTopic,
        group_id='my-group',
        bootstrap_servers=['{kafka_host}:{kafka_port}'.format(kafka_host=kafkaHost, kafka_port=kafkaPort)]
    )
    for m in consumer:
        content=json.loads(m.value)

    print(content)