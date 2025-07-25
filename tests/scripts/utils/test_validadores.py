from app.utils.Validadores import validar_txt_token, validar_correo

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

def test_20():
    """
    Test para validar que la expresión regular reconozca una dirección de correo váida
    """
    RES = validar_correo("test121212.xd@correo.com")
    assert RES == True

def test_21():
    """
    Test para validar que la expresión regular no reconozca una dirección de correo inválida
    """
    RES = validar_correo("test121212.xd@corr2323eo")
    assert RES == False