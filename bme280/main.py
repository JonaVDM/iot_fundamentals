import utime
from machine import Pin, I2C
import bme280
import network
import config
import mqtt
import ujson

# Connect to the internet
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect(config.wifi_ssid, config.wifi_password)

while not net.isconnected():
    pass

print("Connected to the wifi")
print(net.ifconfig())

# Connect to mqtt
connection = mqtt.MQTTClient(
    config.mqtt_client_id,
    config.mqtt_server,
    port=config.mqtt_port,
    user=config.mqtt_user,
    password=config.mqtt_password
)
connection.connect()

# Pin config
led = Pin(config.pin_led, Pin.OUT)
i2c = I2C(config.i2c_id, sda=Pin(config.pin_sda), scl=Pin(config.pin_scl))
bme = bme280.BME280(i2c=i2c)

# The main loop
last_update = utime.time()
while True:
    if last_update + config.mqtt_timeout > utime.time():
        continue
    last_update = utime.time()

    data = {
        "temperature": bme.values[0],
        "pressure": bme.values[1],
        "humidity": bme.values[2]
    }

    print(data)
    led.on()
    connection.publish(config.mqtt_topic, ujson.dumps(data))
    led.off()
