from argon2 import PasswordHasher

def secure_password(password):
	ph = PasswordHasher()
	return ph.hash(password)

def check_password(password, hashed_password):
	ph = PasswordHasher()
	try:
		return ph.verify(hashed_password, password)
	except:
		return False
