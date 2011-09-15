import simplejson
import time
import tornadio
DEBUG = True
CHANNELS = {}

class Channel(object) :

    def __init__(self, ) :
        self._messages = []
        self._callbacks = []

    def message(self, type, nick, msg="") :
        m = { 'type': type, 'timestamp' : int(time.time()), 'text' : msg, 'nick' : nick }

        for cb in self._callbacks :
            cb([m])
        self._callbacks = []

        self._messages.append(m)

    def query(self, cb, since) :
        msgs = [m for m in self._messages if m['timestamp'] > since]
        if msgs :
            return cb(msgs)
        self._callbacks.append(cb)

    def size(self) :
        return 1024

def get_channel(name):
    if name not in CHANNELS.keys():
        CHANNELS[name]=Channel()
    
    return CHANNELS.get( name )
         
class ChatConnection(tornadio.SocketConnection):
    # Class level variable
    participants = {}

    def on_open(self, *args, **kwargs):
        pass

    def on_message(self, message):
        but_me=False

        nick = message.get("nick")

        # join or rejoin 
        if nick not in self.participants or self.participants.get(nick) is not self:
            message = self.join( message )
        
        if "timestamp" not in message:
            message["timestamp"] = time.time()

        if DEBUG:
            print self.participants.keys()
            print message

        self.broadcast( message, self.room, but_me )
    
    def broadcast(self, msg, room=None, but_me=False):
        participants = self.participants
        if but_me:
            del participants[ self.nick ]
        #send_to = filter(lambda p: not p.is_closed, participants.values())
        send_to = participants.values()

        if room:
            send_to = filter(lambda p: p.room is room, send_to)
            channel = get_channel(room)
            channel.message( msg.get("type"), msg.get("nick"), msg.get("msg") )
            
        if DEBUG:
            print send_to
        
        map(lambda p: p.send(msg), self.participants.values())
    
    def send_private( self, msg, to):
        self.participants[to].send(msg)
    
    def join( self, msg):
        self.nick = msg.get("nick")
        self.room = msg.get("room")
        self.participants[self.nick] = self
        msg.update(dict(
            msg = "%s joined" % self.nick,
            type = "info"
        ))
        
        # send missed messages
        channel = get_channel(self.room)
        messages = channel._messages
        self.send( {"messages":messages } )
        
        # send who is there
        self.send(dict(
                    msg ="users "
                    ,type="who"
                    ,who = self.who( self.room )
                    ,nick=self.nick
                    ,room=self.room
                ))
        return msg

    def on_close(self):
        del self.participants[self.nick]
        msg = dict(
            msg ="%s has left." % self.nick 
            ,type="info"
            ,nick=self.nick
            ,room=self.room
        )
        self.broadcast( msg, self.room )
    
    def on_signal(sender, **kwargs):
        print kwargs
        self.broadcast( **kwargs )

    @classmethod
    def send_msg(cls, msssage, room=None):
        cls.broadcast( msg, self.room )

    @classmethod
    def who(cls, room=None) :
        if room:
            return [name for name, participant in cls.participants.items() if participant.room == room ]
        else:
            return cls.participants.keys()



ChatRouter = tornadio.get_router(ChatConnection, resource="chat")
