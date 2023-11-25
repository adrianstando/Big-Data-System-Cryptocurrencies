from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient
import kafka

def test_kafka_connection(bootstrap_servers):
    try:
        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers,'security.protocol': 'plaintext'})
        
        metadata = admin_client.list_topics(timeout=5)
        print("Successfully connected to Kafka!")
        print("Broker Metadata:")
        print(metadata)
        

    except KafkaException as kafka_exception:
        print(f"Failed to connect to Kafka: {kafka_exception}")

def test2():
    consumer = kafka.KafkaConsumer(security_protocol="PLAINTEXT", bootstrap_servers=['localhost:9094'],api_version=(0, 9),consumer_timeout_ms=1000)
    topics = consumer.topics()
    if not topics: 
        raise RuntimeError()

def main():
    bootstrap_servers = 'localhost:9092'

    test_kafka_connection(bootstrap_servers)
    #test2()
if __name__ == "__main__":
    main()