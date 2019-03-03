import time, json
from twilio.rest import Client
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
min_message_delay = 3
msg_in_delay = False
# client = Client(account_sid, auth_token)
# message = client.messages.create(
    # to="=19374896142",
    # from_="+15138153419",
    # body="snek")

# read config file
with open("config.json", "r") as f:
    config = json.load(f)
log_file              = config["suricata_log_file_full_path"]
key_file              = config["suricata_api_key_file"]
account_sid           = config["twilio_account_sid"]
account_number        = config["twilio_account_phone_number"]
test_recipient_number = config["twilio_recipient_number"]

# grab api token. kept seperate so its not included in the repo
with open(key_file, "r") as f:
    auth_token = str(f.read())

# called when file observer notices a file change.
class FileModifiedEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path==log_file:
            handle_file_change(event)

# sets up message and sends through twilio
class TextSender(Client):
    def __init__(self, sid, token, account_phone_number):
        super().__init__(sid, token)
        self.account_phone = account_phone_number
    def send_text(self, recipient_number, message):
        global last_sent_time, msg_in_delay
        if not msg_in_delay:
            msg_in_delay = True
            last_sent_time = curr_time
            messageid = self.messages.create(
                to=recipient_number,
                from_=self.account_phone,
                body=message)
            time.sleep(min_message_delay)
            msg_in_delay = False
            return messageid

# called when log file changes
def handle_file_change(event):
    print(event.src_path)
    sender = TextSender(account_sid, auth_token, account_number)
    sender.send_text(test_recipient_number, "ping sent.")
    # with open(log_file, 'r') as f:
    #   newline = f.readlines()[-1]

# set up watchdog event observer
event_handler = FileModifiedEventHandler()
observed_path = "/var/log/suricata/"
observer = Observer()
observer.schedule(event_handler, observed_path)
observer.start()

# loop until Ctrl+C to quit
try:
    print('Online')
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
