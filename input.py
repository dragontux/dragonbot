import irc
import threading
import tts
import time
import string
import random

ev_handlers = { }
speaker = tts.TextToSpeach()

def add_handler(method, func):
    if method not in ev_handlers:
        ev_handlers.update({method : []})

    ev_handlers[method] += [func]

def irc_event(method):
    def do_add(func):
        add_handler(method, func)

    return do_add

@irc_event("PING")
def ping_reply(server, msg):
    server.send(msg["raw"].replace("I", "O", 3))

@irc_event("PRIVMSG")
def version_ctcp_reply(server, msg):
    if "\01VERSION\01" in msg["message"]:
        server.send_notice(msg["channel"], "\01VERSION desune-bot v0.1\01")
        print("Sent version...")

@irc_event("PRIVMSG")
def ibip_reply(server, msg):
    if msg["message"][:5] == ".bots":
        server.send_message(msg["channel"],
                            "Reporting in! [Python] mobile TTS bot by sugoi " +
                            "(sry for bad connection)")

# TODO: avoid having this as a global variable maybe
last_channel = ""

@irc_event("PRIVMSG")
def chan_message(server, msg):
    # ignore ctcp messages in text-to-speech
    if msg["message"][0] == "\01":
        return

    global last_channel
    speech = ""

    if msg["channel"] == last_channel:
        speech = "%s says %s" % (msg["nick"], msg["message"])

    else:
        last_channel = msg["channel"]
        speech = "from %s: %s says %s" % (msg["channel"],
                                          msg["nick"],
                                          msg["message"])

    print(speech)
    speaker.say(speech)

@irc_event("DISCONNECTED")
def irc_disconnected(server, msg):
    speaker.say("Lost connection...")

@irc_event("CONNECTED")
def irc_connected(server, msg):
    server.identify(server.config["nick"][0])
    speaker.say("Connected to server.")

def do_identify(server):
    server.send_message("NickServ", "identify %s" % server.config["nick-password"][0])

def random_suffix():
    return "".join([random.choice(string.ascii_lowercase) for i in range(5)])

@irc_event("433")
def irc_connected(server, msg):
    new_nick = server.config["nick"][0] + "_" + random_suffix()
    server.nick(new_nick)
    time.sleep(2)
    speaker.say("Reidentifying.")
    nickinfo = (server.config["nick"][0], server.config["nick-password"][0])
    server.send_message("NickServ", "ghost %s %s" % nickinfo)
    time.sleep(2)
    server.send_message("NickServ", "recover %s %s" % nickinfo)
    server.send_message("NickServ", "release %s %s" % nickinfo)
    time.sleep(2)
    server.nick(server.config["nick"][0])
    do_identify(server)
    speaker.say("Contained ghost.")

@irc_event("376")
def handle_end_of_motd(server, msg):
    do_identify(server)

@irc_event("396")
def handle_identified(server, msg):
    server.join(server.config["channels"])
    speaker.say("Joined channels.")

class in_thread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server;

    def do_event_handlers(self, msg):
        print(msg["action"] + " " + msg["raw"])
        if msg["action"] not in ev_handlers:
            return

        for handler in ev_handlers[msg["action"]]:
            handler(self.server, msg)

    def run(self):
        server = self.server

        while True:
            response = server.recv()
            lines    = response.split("\n");

            for line in lines:
                if len(line) < 3:
                    continue

                self.do_event_handlers(irc.parse_message(line))
