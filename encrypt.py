#from simplecrypt import encrypt, decrypt
#import base64
#import os

#this isn't used, due to the fact that pbkdf is VERY SLOW.
#like 20 seconds+ per decrypt
#class c_encryption:
#	def __init__(self):
#		self.encryption_key = os.getenv("pass_key")

#	def encrypt(self, to_encrypt) -> str:
#		encrypted_str = encrypt(self.encryption_key, to_encrypt)
#		return base64.b64encode(encrypted_str).decode("utf8")

#	def decrypt(self, to_decrypt) -> str:
#		decoded_str = base64.b64decode(to_decrypt)
#		return decrypt(self.encryption_key, decoded_str).decode("utf8")