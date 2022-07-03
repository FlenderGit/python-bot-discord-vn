import socket
import json

from Error import vndbException

class VNDB(object):
    protocol = 1
    def __init__(self, clientName, clientVersion, username=None, password=None, debug=False):
        
        self.sock = socket.socket()
        
        if debug: print('Connecting to api.vndb.org...')
        self.sock.connect(('api.vndb.org', 19534))
        if debug: print('Connected !\n')
        
        if debug: print('Authenticating...')
        if (username == None) or (password == None):
            self.sendCommand('login', {'protocol': self.protocol, 'client': clientName,'clientver': float(clientVersion)})
        else:
            self.sendCommand('login', {'protocol': self.protocol, 'client': clientName,'clientver': float(clientVersion), 'username': username, 'password': password})

        res = self.getRawResponse()

        if debug :print("Response : " + res)
        
        if res.find('error ') == 0:
            raise vndbException(json.loads(' '.join(res.split(' ')[1:]))['msg'])

        if debug: print('Authenticated !\n')
        self.cache = {'get': []}
        self.cachetime = 720 #cache stuff for 12 minutes
        

    def close(self):

        """
        Methode to close the socket 
        """
        self.sock.close()	
	
    def get(self, type, flags, filters, options):

        """
        Methode to use the get function of the api
        Usage : get(type, flags, filters, options)
        Return : dictionnary { "num" : len listGame , "items" : { listGame} }
        """

        args = f"{type} {flags} {filters} {options}"    
        
        for item in self.cache['get']:
            if (item['query'] == args):
                return item['results']

        self.sendCommand('get', args)
        #print(self.getRawResponse())
        res = self.getResponse()
        return res[1]
        
    def sendCommand(self, command, args=None):

        whole = ''
        whole += command.lower()
        if isinstance(args, str):
            whole += ' ' + args
        elif isinstance(args, dict):
            whole += ' ' + json.dumps(args,indent = 4)

        whole = '{0}\x04'.format(whole)

        print("cmd : " + whole)

        try:
            self.sock.sendto(whole.encode(),('api.vndb.org', 19534))
        except Exception as e:
            print(e)
	
    def getResponse(self):

        res = self.getRawResponse()
        #print('res : ' + res)
        cmdname = res.split(' ')[0]
        #print('cmdname : ' + cmdname)
        if len(res.split(' ')) > 1:
            args = json.loads(' '.join(res.split(' ')[1:]))

        #print('args : ' + str(args))
	
        if cmdname == 'error':
            if args['id'] == 'throttled':
                raise vndbException('Throttled, limit of 100 commands per 10 minutes')
            else:
                raise vndbException(args['msg'])
        
        return (cmdname, args)
            
    def getRawResponse(self):

        rep = self.sock.recv(4096)

        return rep.decode("UTF-8").replace('\x04', '').strip()

    def getListGameFromId ( self, lsId : int ):
        return self.get('vn', 'basic', f"(id={lsId})", '')['items']


        