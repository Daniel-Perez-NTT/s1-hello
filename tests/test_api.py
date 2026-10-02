from fastapi.testclient import TestClient

from app.main import app, nombres_recibidos

# TestClient simula peticiones HTTP contra la app SIN levantar un servidor real.
client = TestClient(app)


def test_health_devuelve_200():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}


def test_hello_valido_devuelve_200():
    respuesta = client.post("/hello", json={"name": "Dani"})
    assert respuesta.status_code == 200


def test_hello_devuelve_mensaje_correcto():
    respuesta = client.post("/hello", json={"name": "Dani"})
    assert respuesta.json() == {"message": "Hello Dani"}


def test_name_vacio_devuelve_error_de_validacion():
    respuesta = client.post("/hello", json={"name": ""})
    assert respuesta.status_code == 422


def test_name_solo_espacios_devuelve_error_de_validacion():
    # Caso límite: parece lleno pero está vacío
    respuesta = client.post("/hello", json={"name": "   "})
    assert respuesta.status_code == 422


def test_peticion_sin_name_devuelve_error():
    respuesta = client.post("/hello", json={})
    assert respuesta.status_code == 422


def test_hello_guarda_el_nombre_en_memoria():
    nombres_recibidos.clear()  # partimos de un estado limpio
    client.post("/hello", json={"name": "Dani"})
    assert nombres_recibidos == ["Dani"]