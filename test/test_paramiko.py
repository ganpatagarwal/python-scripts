import paramiko

SERVER = raw_input('Please enter an ip address of remote host: ')
USER = raw_input('Please enter your username: ')
PASSWORD = raw_input('Please enter your password: ')

class MYSSHClient():

    def __init__(self, server=SERVER, username=USER, password=PASSWORD):
        self.server = server
        self.username = username
        self.password = password
        self.connection = None
        self.result =  ''
        self.is_error = False


    def do_connect(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(self.server, username=self.username, password=self.password)

    def execute_command(self, command):
        if command:
            print command            
            stdin,stdout,stderr = self.connection.exec_command(command)
            stdin.close()
            error = str(stderr.read())
            if error:
                self.is_error = True
                self.result = error
                print 'error'
            else:
                self.is_error = False
                self.result = str(stdout.read())
                print 'no error'

            print self.result


        else:
            print "no command was entered"

    def do_close(self):
        self.connection.close()

if __name__ == '__main__':
    client = MYSSHClient()
    client.do_connect()
    while 1:
        command = raw_input('cli: ')
        if command == 'q': break
        client.execute_command(command)
    client.do_close()