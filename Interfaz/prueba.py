import hashlib

def codificar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

print(codificar_contrasena("1234"))