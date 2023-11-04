import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(10, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(22,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(27,GPIO.OUT,initial=GPIO.LOW)
# Parámetros de conexión MQTT
broker_address = "192.168.1.67"  # Cambia esto por la dirección IP o el dominio de tu broker MQTT
broker_port = 1884  # Cambia si tu broker está en un puerto diferente
topic = "/CODIGOBARRAS"
error_topic = "/ERROR"
username = "codigobarras"  # Cambia por tu nombre de usuario MQTT
password = "iiot_raspberry"  # Cambia por tu contraseña MQTT


# Función de callback para cuando se conecte al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        GPIO.output(4,GPIO.HIGH)
        sleep(1)
        GPIO.output(10,GPIO.HIGH)
        client.subscribe(error_topic)
    else:
        print("Fallo al conectar con código:", rc)
        GPIO.output(4,GPIO.LOW)
        GPIO.output(10,GPIO.LOW)
        
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == error_topic:
        if payload == "¡CODIGO VALIDO!":
            GPIO.output(22, GPIO.HIGH)
            sleep(2)
            GPIO.output(22, GPIO.LOW)
        elif payload == "¡CODIGO DE BARRAS FUERA DE LA BASE DE DATOS!":
            GPIO.output(27, GPIO.HIGH)
            sleep(2)
            GPIO.output(27, GPIO.LOW)

# Configuración inicial del cliente MQTT
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_start()

item_count = 0

print("Scan the Code... ")

while True:
    scode = str(input())
    
    # Publica el código escaneado al topic "/PRUEBA"
    client.publish(topic, scode)
    
    print("Scanned Barcode is:", scode)
    sleep(2)
    
    item_count += 1
    print("Item Added. Total Item =", item_count)
    sleep(1)

# Asegúrate de detener el loop y desconectar al final (aunque en este caso, el bucle es infinito)
# client.loop_stop()
# client.disconnect()