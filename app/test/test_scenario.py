from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    # ユーザーを登録する
    user_data = {"name": "test_user", "email": "test@example.com", "password": "testpassword"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["name"] == user_data["name"]
    assert created_user["email"] == user_data["email"]
    assert "id" in created_user

    # 登録したユーザーが取得できることを確認する
    response = client.get(f"/user/{created_user['id']}")
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user == created_user

    # ユーザーを更新する
    update_data = {"name": "updated_name", "email": "updated_email@example.com", "password": "updatedpassword"}
    response = client.put(f"/user/{created_user['id']}", json=update_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == update_data["name"]
    assert updated_user["email"] == update_data["email"]
    assert updated_user["password"] == update_data["password"]

    # 更新したユーザーが取得できることを確認する
    response = client.get(f"/user/{created_user['id']}")
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user == updated_user

    # ユーザーを削除する
    response = client.delete(f"/user/{created_user['id']}")
    assert response.status_code == 200
    deleted_user = response.json()
    assert deleted_user == updated_user

    # 削除したユーザーが取得できないことを確認する
    response = client.get(f"/user/{created_user['id']}")
    assert response.status_code == 404
