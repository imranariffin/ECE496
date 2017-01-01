from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from base64 import b64encode, b64decode

def sha1(text):
    s = SHA256.new()
    s.update(text)
    return s.hexdigest()

def Encrypted(text):
	aes = AES.new('JG9A90cqiveJ8K7n', AES.MODE_CFB, 'g4vhFIR1KncRIyvO')
	encrypted_text = aes.encrypt(text)
	return (b64encode(encrypted_text), sha1(text))

def Decrypted(chipertext):
	encrypted_text, match = chipertext[0], chipertext[1]
	aes = AES.new('JG9A90cqiveJ8K7n', AES.MODE_CFB, 'g4vhFIR1KncRIyvO')
	decrypted_text = aes.decrypt(b64decode(encrypted_text))
	return sha1(decrypted_text) == match

