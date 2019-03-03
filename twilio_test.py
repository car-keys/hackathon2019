from twilio.rest import Client
import watchdog
log_file = "/var/log/suricata/fast.log"
key_file = "key.txt"
# client = Client(account_sid, auth_token)

# message = client.messages.create(
    # to="=19374896142",
    # from_="+15138153419",
    # body="snek")    

account_sid = "AC5ec563f144a1a2dc448822e01fffd13f"
with open(key_file, "r") as f:
    auth_token = str(f.read())
account_number = "+15138153419"
test_recipient_number = "15132771334"


class FileModifiedEventHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(event):
        if not event.is_directory:
            handle_file_change(event)


class TextSender(Client):
    def __init__(self, sid, token, account_phone_number):
        super().__init__(sid, token)
        self.account_phone = account_phone_number
    
    def send_text(self, recipient_number, message):
        messageid = self.messages.create(
            to=recipient_number,
            from_=self.account_phone,
            body=message)
        return messageid
        
def handle_file_change(event):
    print(event.src_path)
    # sender = TextSender(account_sid, auth_token, account_number)
    # sender.send_text(test_recipient_number, "ping sent.")
    # with open(log_file, 'r') as f:
    #    newline = f.readlines()[-1]


event_handler = FileModifiedEventHandler()
observed_path = "/var/log/suricata/"
observer = watchdog.Observer()
observer.schedule(event_handler, observed_path)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
    
