"""#ds_messenger.py"""
# Jerald Adriano
# jaadrian@uci.edu
# 91201228

import json
import time
import socket
import ds_protocol
PORT = 3021


class DirectMessage:
    """initalizes the message to be sent"""
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None
        self.port = 3021

    def recep(self):
        """gives recipient"""
        return self.recipient

    def msg(self):
        """gives message"""
        return self.message

    def time(self):
        """gives timestamp"""
        self.timestamp = time.time()
        return self.timestamp


class DirectMessenger:
    """Direct messenger class used to communicate with others"""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        """sends messages to other users"""
        direct_m = DirectMessage()
        direct_m.recipient = recipient
        direct_m.message = message
        direct_m.timestamp = time.time()
        join(self.username, self.password, self.dsuserver)
        self.token = token
        directmsg = {"entry": message, "recipient": recipient,
                     "timestamp": direct_m.timestamp}
        json_obj = json.dumps({"token": token, "directmessage": directmsg})
        if socket_(json_obj, self.dsuserver):
            pass
        else:
            return False
        if Datatuple.type_ == 'ok':
            return True
        return False

    def retrieve_new(self) -> list:
        """retrives new messages for the user"""
        json_obj = directmessage(self.token, 'new')
        if join(self.username, self.password, self.dsuserver):
            pass
        else:
            return False
        self.token = token
        json_obj = directmessage(self.token, 'new')
        socket_(json_obj, self.dsuserver)
        message_lst = Datatuple.message
        return message_lst

    def retrieve_all(self) -> list:
        """retrieves all the messages for the user"""
        if join(self.username, self.password, self.dsuserver):
            pass
        else:
            return False
        self.token = token
        json_obj = directmessage(self.token, 'all')
        socket_(json_obj, self.dsuserver)
        message_lst = Datatuple.message
        return message_lst


def directmessage(tok, message):
    """turns message into json format"""
    json_obj = json.dumps({"token": tok, "directmessage": message})
    return json_obj


def join(username, password, dsuserver):
    """joins the server to get the token"""
    json_obj = json.dumps({"join": {"username": username, "password":
                                    password, "token": ""}})
    return bool(socket_(json_obj, dsuserver))


def socket_(json_obj, dsuserver):
    """Connects and sends a message to the server"""
    global token
    global Datatuple
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((dsuserver, PORT))
            send = client.makefile("w")
            recv = client.makefile("r")
            send.write(json_obj)
            send.flush()
            srv_msg = recv.readline()[:-1]
            Datatuple = ds_protocol.extract_json(srv_msg)
            if 'ok' in Datatuple.type_:
                token = Datatuple.token
            elif 'Invalid' in Datatuple.message:
                return False
            return True
        except (socket.gaierror, TimeoutError, OSError):
            return False


def token_retrieval():
    """Gets the token"""
    return token
