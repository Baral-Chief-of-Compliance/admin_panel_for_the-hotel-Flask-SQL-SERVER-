import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt(13)
    password_hash = bcrypt.hashpw(password.encode("UTF-8"), salt)
    return password_hash.decode("UTF-8")


def check_password(password, password_hash):
    return bcrypt.checkpw(password.encode("UTF-8"), password_hash.encode("UTF-8"))
