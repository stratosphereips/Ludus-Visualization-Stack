from cryptography.fernet import Fernet
import getpass 

## file
fout = "/home/kalin/str/.stuff/"

## key
# key = Fernet.generate_key() # generate key
key = getpass.getpass(prompt='Enter key: ')
cipher_suite = Fernet(key)

## psql
db_user = getpass.getpass(prompt='Enter psql db username: ') 
db_pass = getpass.getpass(prompt='Enter password for {}: '.format(db_user))

## ssh tunnel
us_user = getpass.getpass('Enter user username: ') 
us_pass = getpass.getpass(prompt='Enter password for {}: '.format(us_user))

ssh_pass = getpass.getpass(prompt='Enter ssh tunnel to psql db password: ')

## mysql
bdb_user = getpass.getpass('Enter mysql db username: ') 
bdb_pass = getpass.getpass(prompt='Enter password for {}: '.format(bdb_user))

## elastic
kibana = getpass.getpass('Enter kibana password: ') 
elastic = getpass.getpass('Enter elastic password: ')

creds = [db_user, db_pass, us_user, us_pass, ssh_pass, bdb_user, bdb_pass, kibana, elastic]
fcreds = ['.db_user', '.db_pass', '.us_user', '.us_pass', '.ssh_pass', '.bdb_user', '.bdb_pass', '.kibana', '.elastic']

## write
for i in range(len(creds)):
	open(fout+fcreds[i], 'w').close()
	output_file=open(fout+fcreds[i], 'wb+')
	ciphered_text = cipher_suite.encrypt(bytes(creds[i], "utf-8"))  
	print(ciphered_text) 	
	print(type(ciphered_text))
	output_file.write(ciphered_text)

