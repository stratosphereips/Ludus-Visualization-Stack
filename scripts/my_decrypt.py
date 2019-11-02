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
				decryptedpassword.append(bytes(uncipher_text).decode("utf-8")) #convert to string
#			
	return decryptedpassword

if __name__ == '__main__':
	fin = "/home/kalin/str/.stuff/"
	fcreds = ['.db_user', '.db_pass', '.us_user', '.us_pass', '.ssh_pass', '.bdb_user', '.bdb_pass', '.kibana', '.elastic']
	decrypted = decrypt(fin, fcreds)
	print(decrypted)
