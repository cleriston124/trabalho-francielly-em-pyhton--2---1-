import bcrypt

# transaformação da senha admin para hash
senha_pura = "1234".encode('utf-8')
hash_gerado = bcrypt.hashpw(senha_pura, bcrypt.gensalt())


print(hash_gerado.decode('utf-8'))
