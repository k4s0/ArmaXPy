def scriptHash(string):
    import hashlib
    hash_object = hashlib.sha512(string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig
