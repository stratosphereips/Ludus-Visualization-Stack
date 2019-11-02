import paramiko
import time
"ssh -i /home/cznic/.ssh/id_rsa -NT -L 5432:ludus.sn.turris.cz:5432 ludus@bouncer.turris.cz"
from cryptography.fernet import Fernet
import getpass 
  
def decrypt(fin, fcreds):

        key = getpass.getpass(prompt='Enter key: ') 
        cipher_suite = Fernet(key)

        encryptedpwd = []
        decryptedpassword = []
        for f in fcreds:
                with open(fin+f, 'rb') as fins:
                        for line in fins:
                                encryptedpwd.append(line)
                                uncipher_text = (cipher_suite.decrypt(encryptedpwd[-1]))
                                decryptedpassword.append(bytes(uncipher_text).decode("utf-8"))
#
        return decryptedpassword

def keep_alive(hostname, password, username, port, k):
	remote_port = 5432
	local_port  = 5432
	ssh_host    = "0.0.0.0"
	ssh_port    = 22
	transport = paramiko.Transport((ssh_host, ssh_port))

	# Command for paramiko-1.7.7.1
	transport.connect(hostkey  = None,
		              username = user,
		              password = password,
		              pkey     = k)
	try:
		forward_tunnel(local_port, remote_host, remote_port, transport)
	except KeyboardInterrupt:
		print('Port forwarding stopped.')
		sys.exit(0)
		              
                  
if __name__ == '__main__':
	
	fin = "/home/kalin/str/.stuff/"
	fcreds = ['.ssh_pass']
	password = decrypt(fin, fcreds)[0]
	remote_host = "ludus.sn.turris.cz"
	username = "ludus@bouncer.turris.cz"
	port = 5432
	k = paramiko.RSAKey.from_private_key_file("/home/cznic/.ssh/id_rsa")
	keep_alive(remote_host, password, username, port, k)
	
