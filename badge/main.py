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

current_frame = 0

led_rows = [
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000,
    0b0000000
]
async def publish_led_row(client, row, cols):
    await client.publish(TOPIC_PREFIX + "/leds/spiral/row", pack("BB", row, cols), qos=1)

async def apply_led(client, row, col):
    r = row - 1
    c = col - 1
    mask = (1 << c)

    led_rows[r] |= mask
    print(bin(led_rows[r]))
    await publish_led_row(client, row, led_rows[r])
    await asyncio.sleep(2)

    led_rows[r] &= 0b111111 ^ mask
    print(bin(led_rows[r]))
    await publish_led_row(client, row, led_rows[r])
    
    


async def messages(client):
    async for topic, msg, retained in client.queue:
        (request_type, row, col) = unpack("BBB", msg)
        print(topic.decode(), request_type, row, col, retained)
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
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    n = 0
    while True:
        await asyncio.sleep(5)
        print("publish", n)
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