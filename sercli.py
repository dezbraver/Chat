from socket import socket

class Sercli:
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def servidor(self):
		with socket(AF_INET, SOCK_STREAM) as s:
			s.bind((self.host, self.port))
			s.listen(5)
			print("Aguardando Conexões...\n")
			while True:
				con, cli = s.accept()
				with con:
					

	
