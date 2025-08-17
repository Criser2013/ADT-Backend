from app.utils.Validadores import *

def test_3():
    """
    Test para validar que la función reconozca correctamente un token
    bien estructurado.
    """
    TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ3YWU0OWM0YzlkM2ViODVhNTI1NDA3MmMzMGQyZThlNzY2MWVmZTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoibm8gYyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMaUs4YkJ5d2ZGaEJsaUk2Tkh0M3lrRkh4SWFZMDRHT0tUUVNoaU1hbUVqMXZxbnNqTz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9oYWR0LTQ2MjBhIiwiYXVkIjoiaGFkdC00NjIwYSIsImF1dGhfdGltZSI6MTc1MTk5MDY1NywidXNlcl9pZCI6Im5TbHZrRGJ4TkJVWTVXb0t3VW1CV0dOSlFIdjIiLCJzdWIiOiJuU2x2a0RieE5CVVk1V29Ld1VtQldHTkpRSHYyIiwiaWF0IjoxNzUxOTkwNjU3LCJleHAiOjE3NTE5OTQyNTcsImVtYWlsIjoibG9xdWVuZG8uY3Jpc3RpYW4uNzhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDQzNDE4NDA1ODM4NjkzMjU2OTQiXSwiZW1haWwiOlsibG9xdWVuZG8uY3Jpc3RpYW4uNzhAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.yYzwp-fUmMj8I7qiVjQ4t2n5AFsRw-V2qAONehEwhQ7aYc46A_49ukpKpC4cJkPXFV4R5yKD0NEdgcZ-cJnBEYGSy8Py__WDFFo1y-gmih5w3nyheRySJFNxDm-_7zLLfCVpmOM2wAbU9hAYjN5qzvHfx3aETN3ttKUSlxf_a8m6vOB4KPN3D6lYgrHoq76_o41FWtlPM0xCHWTxh98YcjdfLxghozDXhUWvGHjgvvLRWM6aJbqASRI7mARLW5clbnU1UT6cQbgoMyyPbDAuXzvcJOrDusnyJQxOYzM4cYesyrzMnqFAlP-YJbsQa5drlSI4RMzo-a357yUiZbLKfw"
    RES = validar_txt_token(TOKEN)
    assert RES == True

def test_4():
    """
    Test para validar que la función no reconozca un token de longitud pequeña
    pero con caracteres inválidos.
    """
    token = "a" * 800
    token += "@hola+++'''"
    RES = validar_txt_token(token)
    assert RES == False

def test_58():
    """
    Test para validar que la función reconozca un UID válido.
    
    """
    uid = "nSlvkDbxNBUY5WoKwUmBWGNJQHv2"
    RES = validar_uid(uid)
    assert RES == True

def test_59():
    """
    Test para validar que la función reconozca un UID inválido.
    """
    uid = "usuario@cor1212reo.com@"
    RES = validar_uid(uid)
    assert RES == False

def test_75():
    """
    Test para validar que la función convierta el caracter '*' en una expresión
    regular que admita cualquier carácter.
    """
    RES = proc_origen("*")
    assert RES == r"([\w|-|_|.|/|:])*"

def test_76():
    """
    Test para validar que la función convierta el caracter '*' en una expresión
    regular que admita cualquier carácter en una subcadena
    """
    RES = proc_origen("https://dominio.subdominio1.*.com")
    assert RES == r"https://dominio.subdominio1.([\w|-|_|.|/|:])*.com"

def test_77():
    """
    Test para validar que la función tome como válidos todos dominios que coincidan con la
    lista (tiene elementos con comodines)
    """
    RES = validar_origen("https://dominio.subdominio1.hola.com", ["https://dominio.subdominio1.*.com"])
    assert RES == True

def test_78():
    """
    Test para validar que la función tome como válidos todos los dominios
    """
    RES = validar_origen("https://dominio.subdominio1.hola.com", ["*"])
    assert RES == True

def test_79():
    """
    Test para validar que la función no tome como válido un dominio no autorizado
    """
    RES = validar_origen("https://dominio.subdominio1.hola.com", ["http://dominio.subdominio4.com"])
    assert RES == False