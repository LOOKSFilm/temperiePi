from sense_hat import SenseHat
import time
from datetime import datetime
import json
import threading
import paramiko
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

sense = SenseHat()
#temp = round(sense.get_temperature(), 1)
server_nodes = ["10.0.77.1", "10.0.77.10", "10.0.77.11", "10.0.77.12", "10.0.77.13", "10.0.77.14", "10.0.77.16"]
def mesure_temp():
    while True:
        global temperature
        temperature = round(sense.get_temperature(), 1)
        print(temperature)
        sense.set_rotation(180) 
        sense.show_message(str(temperature), scroll_speed=0.1, text_colour=[50,255,50])
thread_mesure_temp = threading.Thread(target=mesure_temp)
thread_mesure_temp.start()

def ping_servers():
    for server_node in server_nodes:
        response = os.system("ping -c 1 " + server_node)
        print(response)
thread_ping = threading.Thread(target=ping_servers)
thread_ping.start()
def shutdown():
    #server_nodes = ["10.0.77.12"]
    info = list()
    for server_node in server_nodes:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server_node, username="editshare", password="changeme0479")

        #command = "sudo shutdown -h 10"
        command = 'hostname'
        stdin, stdout, stderr = client.exec_command(command)

        err = stderr.read().decode('utf-8')
        msg = stdout.read().decode('utf-8')
        server_info = dict()
        server_info["ip"] = server_node
        server_info["message"] = msg
        server_info["error"] = err
        info.append(server_info)
        stdout.channel.recv_exit_status()

        client.close()
    return info

def write_mail(receiver, subject, text, cc=None):

    sender = "info@killswit.ch"
    #cc_email = "otherperson@example.com"
    smtp_server = "localhost"  # Use the hostname or IP address of your SMTP server

    # Create a multipart message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg["Cc"] = cc

    # Attach the HTML body of the email
    msg.attach(MIMEText(text, "html"))

    # Send the email
    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(sender, [receiver, cc], msg.as_string())
        #server.sendmail(sender, [receiver], msg.as_string())

def action():
    shutdown_ini = False
    warning = False
    i = 0
    try:
        with open("temperiePi/temperature_log.json", "r") as f:
            save_temp_dict = json.load(f)
    except:
        save_temp_dict = dict()

    while True:
        if temperature >= 40 and shutdown_ini == False:
            response = shutdown()
            shutdown_ini = True
            log = str()
            for info in response:
                log += f'{info["ip"]}: {info["error"]}'
            text = f"""
            <body>
                <p>Es ist zu heiß im Serverraum ({temperature}°C). Die Server werden in 10min herunter gefahren:</p>
                <pre>{log}</pre>
                <br><br>
                <p>Um shutdown abzubrechen:</p>
                <pre>ssh -t postpro@killswitch 'bash -ic "cancel_shutdown"'</pre>
            </body>
            """
            write_mail("lewinske@looks.film", "SERVER SHUTDOWN", text, cc="ritter@looks.film")
            #write_mail("lewinske@looks.film", "SERVER SHUTDOWN", text)
        elif temperature >= 35 and warning == False:
            warning = True
            text = f"""
            <body>
                <p>Es ist verdächtig heiß im Serverraum ({temperature}°C)! Ist alles ok?</p>
                <br><br>
                <p>Server werden automatisch herunter gefahren wenn 40°C erreicht sind.</p>
            </body>
            """
            write_mail("lewinske@looks.film", "SERVER WARNING", text, cc="ritter@looks.film")
            #write_mail("lewinske@looks.film", "SERVER SHUTDOWN", text)
        elif temperature <= 34:
            shutdown_ini = False
            warning = False
        if i == 60:
            timestamp = datetime.now().strftime('%H:%M:%S')
            save_temp_dict[timestamp] = temperature
            if len(save_temp_dict) > 720:
                # Entferne die ältesten Werte
                keys_to_remove = list(save_temp_dict.keys())[:-720]
                for key in keys_to_remove:
                    save_temp_dict.pop(key)
            with open("temperiePi/temperature_log.json", "w") as f:
                json.dump(save_temp_dict, f, indent=4)
            i = 0
        i += 1
        time.sleep(1)

thread_action = threading.Thread(target=action)
thread_action.start()