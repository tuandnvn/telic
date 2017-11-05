'''
Created on Sep 8, 2014

@author: Tuan
'''
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import json as js
class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 2346)))
     
    def parse(self, text):
        return js.loads(self.server.parse(text))