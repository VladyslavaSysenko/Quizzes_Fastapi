from httpx import AsyncClient


async def test_bad_create_user__not_password(ac: AsyncClient):
    payload = {
        "user_password": "",
        "user_password_repeat": "",
        "user_email": "test@test.com",
        "user_username": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Password must be 4+ characters long"


async def test_bad_create_user__low_password(ac: AsyncClient):
    payload = {
        "user_password": "tet",
        "user_password_repeat": "tet",
        "user_email": "test@test.com",
        "user_username": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Password must be 4+ characters long"


async def test_bad_create_user__dont_match(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "tess",
        "user_email": "test@test.com",
        "user_username": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Passwords do not match"


async def test_bad_create_user__no_valid_email(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "tess",
        "user_email": "test",
        "user_username": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get("msg") == "value is not a valid email address"


async def test_create_user_one(ac: AsyncClient):
    payload = {
        "user_password": "test1",
        "user_password_repeat": "test1",
        "user_email": "test1@test.com",
        "user_username": "test1",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1


async def test_bad_create_user__email_exist(ac: AsyncClient):
    payload = {
        "user_password": "testt",
        "user_password_repeat": "testt",
        "user_email": "test1@test.com",
        "user_username": "test2",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Email already registered"


async def test_create_user_two(ac: AsyncClient):
    payload = {
        "user_password": "test2",
        "user_password_repeat": "test2",
        "user_email": "test2@test.com",
        "user_username": "test2",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 2


async def test_create_user_three(ac: AsyncClient):
    payload = {
        "user_password": "test3",
        "user_password_repeat": "test3",
        "user_email": "test3@test.com",
        "user_username": "test3",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 3


async def test_create_user_four(ac: AsyncClient):
    payload = {
        "user_password": "test4",
        "user_password_repeat": "test4",
        "user_email": "test4@test.com",
        "user_username": "test4",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 4


async def test_create_user_five(ac: AsyncClient):
    payload = {
        "user_password": "test5",
        "user_password_repeat": "test5",
        "user_email": "test5@test.com",
        "user_username": "test5",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 5


async def test_create_user_six(ac: AsyncClient):
    payload = {
        "user_password": "test6",
        "user_password_repeat": "test6",
        "user_email": "test6@test.com",
        "user_username": "test6",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 6


# =================================


async def test_bad_try_login(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "test_bad")
    assert response.status_code == 422
    assert response.json().get('detail') == 'Incorrect password'


async def test_try_login_one(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "test1")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_try_login_two(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "test2")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_try_login_three(ac: AsyncClient, login_user):
    response = await login_user("test3@test.com", "test3")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_try_login_four(ac: AsyncClient, login_user):
    response = await login_user("test4@test.com", "test4")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_try_login_five(ac: AsyncClient, login_user):
    response = await login_user("test5@test.com", "test5")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'

async def test_try_login_six(ac: AsyncClient, login_user):
    response = await login_user("test6@test.com", "test6")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_auth_me_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_username') == "test1"
    assert response.json().get('result').get('user_email') == "test1@test.com"
    assert response.json().get('result').get('user_id') == 1
    assert response.json().get('result').get('user_password') == None


async def test_auth_me_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_username') == "test2"
    assert response.json().get('result').get('user_email') == "test2@test.com"
    assert response.json().get('result').get('user_id') == 2
    assert response.json().get('result').get('user_password') == None


async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": "Bearer retretwetrt.rqwryerytwetrty",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail') == "Incorrect token"


# =====================================================


async def test_get_users_list(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 6


async def test_get_users_list_unauth(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/2", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_username') == "test2"
    assert response.json().get('result').get('user_email') == "test2@test.com"
    assert response.json().get('result').get('user_id') == 2
    assert response.json().get('result').get('user_password') == None


async def test_get_user_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/user/2")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_user_by_id__not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/100", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_bad_update_user_one__not_your_acc(ac: AsyncClient, users_tokens):
    payload = {
        "user_username": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/2", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_update_user_one(ac: AsyncClient, users_tokens):
    payload = {
        "user_username": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/1", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1


async def test_get_user_by_id_updated(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == 'test1@test.com'
    assert response.json().get("result").get("user_username") == 'test1NEW'
    assert response.json().get('result').get('user_password') == None


async def test_bad_delete_user_five__not_your_account(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/user/5", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_delete_user_five(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test5@test.com']}",
    }
    response = await ac.delete("/user/5", headers=headers)
    assert response.status_code == 200


async def test_get_users_list_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 5