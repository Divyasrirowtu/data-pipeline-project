import json
import logging
import os

from kafka import KafkaConsumer, KafkaProducer

from app.cdc.processors.event_processor import CDCEventProcessor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:29092",
)

INPUT_TOPIC = os.getenv(
    "CDC_INPUT_TOPIC",
    "ledger.public.accounts",
)

VALID_TOPIC = os.getenv(
    "CDC_VALID_TOPIC",
    "ledger.valid.events",
)

DLQ_TOPIC = os.getenv(
    "CDC_DLQ_TOPIC",
    "ledger.dlq",
)


def create_consumer():
    return KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="ledger-cdc-processor",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: value.decode("utf-8"),
    )


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def run():
    consumer = create_consumer()
    producer = create_producer()

    processor = CDCEventProcessor()

    logger.info("CDC processor started")
    logger.info("Input topic: %s", INPUT_TOPIC)

    try:
        for message in consumer:
            result = processor.process(message.value)

            if result["valid"]:
                producer.send(
                    VALID_TOPIC,
                    result["event"],
                )

                logger.info(
                    "Valid CDC event published to %s",
                    VALID_TOPIC,
                )

            else:
                producer.send(
                    DLQ_TOPIC,
                    {
                        "original_event": result["event"],
                        "error": result["reason"],
                    },
                )

                logger.warning(
                    "Invalid CDC event sent to %s: %s",
                    DLQ_TOPIC,
                    result["reason"],
                )

            producer.flush()

    finally:
        consumer.close()
        producer.close()


if __name__ == "__main__":
    run()