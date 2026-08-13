import pytest
from utils.Validadores import *


@pytest.mark.parametrize(
    "token,respuesta_esperada",
    [
        (
            "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ3YWU0OWM0YzlkM2ViODVhNTI1NDA3MmMzMGQyZThlNzY2MWVmZTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoibm8gYyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMaUs4YkJ5d2ZGaEJsaUk2Tkh0M3lrRkh4SWFZMDRHT0tUUVNoaU1hbUVqMXZxbnNqTz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9oYWR0LTQ2MjBhIiwiYXVkIjoiaGFkdC00NjIwYSIsImF1dGhfdGltZSI6MTc1MTk5MDY1NywidXNlcl9pZCI6Im5TbHZrRGJ4TkJVWTVXb0t3VW1CV0dOSlFIdjIiLCJzdWIiOiJuU2x2a0RieE5CVVk1V29Ld1VtQldHTkpRSHYyIiwiaWF0IjoxNzUxOTkwNjU3LCJleHAiOjE3NTE5OTQyNTcsImVtYWlsIjoibG9xdWVuZG8uY3Jpc3RpYW4uNzhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDQzNDE4NDA1ODM4NjkzMjU2OTQiXSwiZW1haWwiOlsibG9xdWVuZG8uY3Jpc3RpYW4uNzhAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.yYzwp-fUmMj8I7qiVjQ4t2n5AFsRw-V2qAONehEwhQ7aYc46A_49ukpKpC4cJkPXFV4R5yKD0NEdgcZ-cJnBEYGSy8Py__WDFFo1y-gmih5w3nyheRySJFNxDm-_7zLLfCVpmOM2wAbU9hAYjN5qzvHfx3aETN3ttKUSlxf_a8m6vOB4KPN3D6lYgrHoq76_o41FWtlPM0xCHWTxh98YcjdfLxghozDXhUWvGHjgvvLRWM6aJbqASRI7mARLW5clbnU1UT6cQbgoMyyPbDAuXzvcJOrDusnyJQxOYzM4cYesyrzMnqFAlP-YJbsQa5drlSI4RMzo-a357yUiZbLKfw",
            True,
        ),
        (("a" * 800) + "@hola+++'''", False),
    ],
    ids=["test_3", "test_4"],
)
def test_validar_txt_token(token, respuesta_esperada):
    """
    Test para validar que la función reconozca correctamente un token
    bien estructurado.
    """
    RES = validar_txt_token(token)
    assert RES == respuesta_esperada


@pytest.mark.parametrize(
    "uid,respuesta_esperada",
    [("nSlvkDbxNBUY5WoKwUmBWGNJQHv2", True), ("usuario@cor1212reo.com@", False)],
    ids=["test_58", "test_59"],
)
def test_validar_uid(uid, respuesta_esperada):
    """
    Test para validar que la función reconozca un UID válido.
    """
    RES = validar_uid(uid)
    assert RES == respuesta_esperada


@pytest.mark.parametrize(
    "texto,respuesta_esperada",
    [
        ("*", r"([\w|-|_|.|/|:])*"),
        (
            "https://dominio.subdominio1.*.com",
            r"https://dominio.subdominio1.([\w|-|_|.|/|:])*.com",
        ),
    ],
    ids=["test_75", "test_76"],
)
def test_proc_origen(texto, respuesta_esperada):
    """
    Test para validar que la función convierta el caracter '*' en una expresión
    regular que admita cualquier carácter.
    """
    RES = proc_origen(texto)
    assert RES == respuesta_esperada


@pytest.mark.parametrize(
    "texto,origenes,respuesta_esperada",
    [
        (
            "https://dominio.subdominio1.hola.com",
            ["https://dominio.subdominio1.*.com"],
            True,
        ),
        ("https://dominio.subdominio1.hola.com", ["*"], True),
        (
            "https://dominio.subdominio1.hola.com",
            ["http://dominio.subdominio4.com"],
            False,
        ),
    ],
    ids=["test_77", "test_78", "test_79"],
)
def test_validar_origen(texto, origenes, respuesta_esperada):
    """
    Test para validar que la función tome como válidos todos dominios que coincidan con la
    lista (tiene elementos con comodines)
    """
    RES = validar_origen(texto, origenes)
    assert RES == respuesta_esperada
