import hashlib

# 用于加密密码，避免在数据库中明文保存密码
def encrypt(pwd):
    sha = hashlib.sha256(pwd.encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted