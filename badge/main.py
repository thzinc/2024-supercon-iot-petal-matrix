from mqtt_as import MQTTClient, config
import asyncio
from struct import pack, unpack
from constants import WIFI_SSID, WIFI_PASSWORD, MQTT_HOST, DEVICE_ID

REQUEST_TYPE_TOUCH = 1

config["ssid"] = WIFI_SSID
config["wifi_pw"] = WIFI_PASSWORD
config["server"] = MQTT_HOST

TOPIC_PREFIX = "thzinc/2024-supercon/" + DEVICE_ID
print("Using " + TOPIC_PREFIX)

led_rows = [
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
]
led_changed = False


async def apply_led(client, row, col):
    global led_changed
    global led_rows

    r = row - 1
    c = col - 1
    mask = 1 << c

    led_rows[r] |= mask

    petal_bus.writeto_mem(PETAL_ADDRESS, row, bytes([led_rows[r]]))
    led_changed = True

    await asyncio.sleep(2)

    led_rows[r] &= 0b111111 ^ mask
    petal_bus.writeto_mem(PETAL_ADDRESS, row, bytes([led_rows[r]]))
    led_changed = True


async def publish_led_rows(client):
    global led_changed
    global led_rows

    while True:
        if led_changed:
            led_changed = False
            await asyncio.gather(
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 1, led_rows[0]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 2, led_rows[1]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 3, led_rows[2]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 4, led_rows[3]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 5, led_rows[4]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 6, led_rows[5]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 7, led_rows[6]), qos=1
                ),
                client.publish(
                    TOPIC_PREFIX + "/leds/spiral/row", pack("BB", 8, led_rows[7]), qos=1
                ),
            )
        await asyncio.sleep(0.2)


async def messages(client):
    async for topic, msg, retained in client.queue:
        (request_type, row, col) = unpack("BBB", msg)
        if request_type == REQUEST_TYPE_TOUCH:
            if row > 8 or col > 7:
                pass
            asyncio.create_task(apply_led(client, row, col))


async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe(
            TOPIC_PREFIX + "/requests/#",
            1,
        )


async def main(client):
    await client.connect()
    for coroutine in (up, messages, publish_led_rows):
        asyncio.create_task(coroutine(client))
    n = 0
    while True:
        await asyncio.sleep(5)
        # If WiFi is down the following will pause for the duration.
        await client.publish(TOPIC_PREFIX + "/liveness", "{}".format(n), qos=1)
        n += 1


config["queue_len"] = 16
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()
