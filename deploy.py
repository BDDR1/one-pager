import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HR_HOST")
PORT = int(os.getenv("HR_PORT"))
USERNAME = os.getenv("HR_USER")
PASSWORD = os.getenv("HR_PASS")

LOCAL_DIR = "."
REMOTE_DIR = "public.www"

transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, password=PASSWORD)

sftp = paramiko.SFTPClient.from_transport(transport)

def upload_dir(local, remote):
    for item in os.listdir(local):
        local_item = os.path.join(local, item)
        remote_item = remote + "/" + item

        if os.path.isdir(local_item):
            try:
                sftp.mkdir(remote_item)
            except:
                pass
            upload_dir(local_item, remote_item)
        else:
            print("Uploading", item)
            sftp.put(local_item, remote_item)

upload_dir(LOCAL_DIR, REMOTE_DIR)

sftp.close()
transport.close()

print("Deploy klaar")