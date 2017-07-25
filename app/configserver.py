import configparser

class ConfigServer():
    def __init__(self,configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)


    def config_server(self):
        host = self.config['SERVER']['ipaddr']
        if len(host) == 0:
            host = ''
        port = int(self.config['SERVER']['listen_port'])
        return(host,port)

    def get_output(self):
        return self.config['SERVER']['output_dir']
