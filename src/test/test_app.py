from .. import main
from fastapi.testclient import TestClient

client = TestClient(main.app)
token = None

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_url_expired():
    response = client.get("/1d")
    assert response.status_code == 403
    assert response.json() == {"detail": {"error": "url expired"}}


def test_url_404():
    response = client.get("/404")
    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "Page not found"}}


def test_user_login_success():
    response = client.post(
        "/auth/login/", data={"username": "string", "password": "string"})
    token = response.json()
    assert token is not None
    assert response.status_code == 200


def test_user_login_failed():
    response = client.post(
        "/auth/login/", data={"username": "wrong", "password": "fakedata"})
    token = response.json()
    assert token == {'detail': {'Error': 'Username or password incorrect'}}
    assert response.status_code == 401


def test_protected_route():
    response = client.get("/auth/me/")
    assert response.status_code == 401


def user_login_success(test_user):
    response = client.post("/auth/login/", data=test_user)
    print(response)

    return response.json()["access_token"]


def test_create_url_no_valid_site():
    token = user_login_success({"username": "string", "password": "string"})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/shorturl/create", headers=headers, data={"url": "not_a_site"})

    assert response.status_code == 422


def test_create_already_exist_alias():
    token = user_login_success({"username": "string", "password": "string"})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/shorturl/create", headers=headers, data={
                           "url": "http://127.0.0.1:8000/docs#/Url%20Shortener%20Dashboard/create_url_shorturl_create_post", "alias": "1d"})

    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "error": "please choice another alias its already taken by someone"
        }
    }


def test_delete_url():
    token = user_login_success({"username": "string", "password": "string"})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/shorturl/delete/",
                           headers=headers, data={"item_id": "1d"})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'} 

def test_delete_url_vaild_id():
    token = user_login_success({"username": "string", "password": "string"})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/shorturl/delete/",
                           headers=headers, data={"item_id": "0"})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'} 
