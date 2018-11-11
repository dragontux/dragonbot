import socket
import time

# XXX: (dis)connection messages so losses in connection can be hooked
DISCONNECTED_MSG = "DISCONNECTED :lost connection\n"
CONNECTED_MSG = "CONNECTED :connected to server\n"
INVALID_MSG = "INVALID :Invalid message\n"

def parse_host(host_str):
    nick = ""

    try:
        nick = host_str[host_str.index(":")+1 : host_str.index("!")]
    except ValueError:
        pass

    return { "nick": nick }

def parse_message(message):
    words = message.split(" ")

    ret = {
        "action": "INVALID",
        "channel": "None",
        "nick": "None",
        "raw": message,
    }

    if len(message) > 0 and message[0] == ":":
        ret.update(parse_host(words[0]))
        words = words[1:]

    if len(words) > 2:
        ret.update({ "channel": words[1] })

    if len(words) > 0:
        action = words[0]
        ret.update({ "action": action, })

    try:
        temp = message
        temp = temp[temp.index(":")+2:]
        temp = temp[temp.index(":")+1:]
        ret.update({ "message": temp, })

    except (ValueError, IndexError):
        ret.update({ "message": "$<-NaN>", })

    return ret

class irc_server( ):
    def __init__(self, config):
        self.is_connected = False
        self.notified_disconnect = True
        self.server = config["server"][0]
        self.port = 6667
        self.config = config

    def connect(self):
        if not self.is_connected:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                self.sock.connect((self.server, self.port))
                self.sock.settimeout(200)

                # TODO: check that we're actually connected
                self.is_connected = True

            except Exception as e:
                print(e)

    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            self.sock.close()

    def try_reconnect(self):
        if not self.is_connected:
            print("Trying to reconnect...")
            self.connect()

    def reconnect(self):
        while not self.is_connected:
            self.try_reconnect()
            time.sleep(20)

    def send(self, message):
        self.reconnect()

        print(">> sending " + message)
        try:
            if self.sock.send(bytes(message, "UTF-8")) == 0:
                self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()

    def recv(self):
        self.reconnect()
        buf = bytes()

        if self.is_connected and self.notified_disconnect:
            self.notified_disconnect = False
            return CONNECTED_MSG

        while "\n".encode() not in buf:
            try:
                temp = self.sock.recv(1024)
                buf += temp

                if len(temp) == 0:
                    raise Exception()

            except Exception as e:
                # no longer connected, need to close socket
                # and try to reconnect...
                self.disconnect()
                buf += "\n".encode()
                buf += DISCONNECTED_MSG.encode()
                self.notified_disconnect = True
                break

        #print(buf)
        try:
            return buf.decode()
        except Exception as e:
            return INVALID_MSG

    def send_message( self, channel, message ):
        self.send("PRIVMSG %s :%s\r\n" % (channel, message))

    def send_notice( self, channel, message ):
        self.send("NOTICE %s :%s\r\n" % (channel, message))

    def identify( self, nick ):
        self.send("USER %s %s %s :%s\r\n" % (nick, nick, nick, nick))
        self.send("NICK %s\r\n" % (nick))

    def nick( self, nick ):
        self.send( "NICK %s\r\n" % (nick))

    def join( self, channels ):
        for thing in channels:
            self.send( "JOIN %s\r\n" % (thing))

    def part( self, channels ):
        for thing in channels:
            self.send("PART %s\r\n" % (thing))

    def quit( self, message ):
        self.send("QUIT :" + message + "\r\n")
        self.sock.close()
