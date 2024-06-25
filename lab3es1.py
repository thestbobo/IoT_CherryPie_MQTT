import paho.mqtt.client as mqtt
import requests
import json
import time


mqtt_broker = "test.mosquitto.org"
temperature_topic = "/tiot/group/temperature"
led_topic = "/tiot/group/led"
device_id = "arduino_device_01"


catalog_url = "http://127.0.0.1:5000/api/catalog"
renew_url = catalog_url + "/renew"



def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(led_topic)


def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        if "e" in data and len(data["e"]) > 0 and "v" in data["e"][0]:
            led_state = data["e"][0]["v"]
            print(f"Setting LED state to: {led_state}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def register_device():
    payload = {
        "id": device_id,
        "temp_topic": temperature_topic,
        "led_topic": led_topic
    }
    response = requests.post(catalog_url, json=payload)
    if response.status_code == 200:
        print(f"Device registered: {response.json()}")
    else:
        print(f"Failed to register device: {response.status_code}, {response.text}")


def renew_subscription():
    payload = {
        "id": device_id
    }
    response = requests.put(renew_url, json=payload)
    if response.status_code == 200:
        print(f"Subscription renewed: {response.json()}")
    else:
        print(f"Failed to renew subscription: {response.status_code}, {response.text}")



def publish_temperature(client):
    temperature = 25.0
    payload = {
        "e": [
            {
                "n": "temperature",
                "u": "C",
                "v": temperature
            }
        ]
    }
    client.publish(temperature_topic, json.dumps(payload))
    print(f"Published temperature: {temperature}")


def main():

    client = mqtt.Client()
    print("connecting")
    time.sleep(3)
    client.on_connect = on_connect
    print("connesso")
    client.on_message = on_message
    client.connect(host=mqtt_broker, port=1883, keepalive=60)


    register_device()


    last_publish_time = time.time()
    last_renew_time = time.time()

    try:
        while True:
            client.loop()

            current_time = time.time()
            if current_time - last_publish_time >= 10:
                publish_temperature(client)
                last_publish_time = current_time

            if current_time - last_renew_time >= 60:
                renew_subscription()
                last_renew_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()


if __name__ == "__main__":
    main()