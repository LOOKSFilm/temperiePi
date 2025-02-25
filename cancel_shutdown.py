import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import paramiko


def shutdown():
    server_nodes = ["10.0.77.1", "10.0.77.10", "10.0.77.11", "10.0.77.12", "10.0.77.13", "10.0.77.14", "10.0.77.16"]
    #server_nodes = ["10.0.77.12"]
    info = list()
    for server_node in server_nodes:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server_node, username="editshare", password="changeme0479")

        command = "sudo shutdown -c"
        #command = 'ls'
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
        print(f"Shutdown canceled on {server_node}")
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
        #server.sendmail(sender_email, [receiver_email, cc_email], msg.as_string())
        server.sendmail(sender, [receiver], msg.as_string())

response = shutdown()
log = str()
for info in response:
    log += f'{info["ip"]}<br>'
text = f"""
<body>
    <p>Shutdown canceled on:</p>
    <pre>{log}</pre>
</body>
"""
write_mail("lewinske@looks.film", "SHUTDOWN CANCELED", text)