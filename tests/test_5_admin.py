from httpx import AsyncClient


async def test_create_admin_not_auth(ac: AsyncClient):
    payload = {
        "user_id": 1
    }
    response = await ac.post('/company/2/admin', json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_create_admin_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_create_admin_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin', headers=headers, json=payload)
    assert response.status_code == 404, response.json()
    assert response.json().get('detail') == "User not found"


async def test_create_admin_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 2,
    }
    response = await ac.post('/company/100/admin', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_create_admin_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 1,
    }
    response = await ac.post('/company/2/admin', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_create_admin_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 4
    }
    response = await ac.post('/company/1/admin', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_create_admin_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 3
    }
    response = await ac.post('/company/2/admin', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


# admin-list
async def test_admin_list_not_auth(ac: AsyncClient):
    response = await ac.get('/company/2/admins')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_admin_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/admins', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_admin_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 2


# admin-remove
async def test_admin_remove_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/2/admin/1')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_admin_remove_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/2/admin/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_admin_remove_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/admin/1', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company not found'


async def test_admin_remove_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/2/admin/1', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_admin_remove_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/2/admin/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_admin_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 1


async def test_admin_list_control(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/company/1/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 1


# GIVE OWNERSHIP


async def test_give_ownership_not_auth(ac: AsyncClient):
    response = await ac.post('/company/2/ownership')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_give_ownership_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 3
    }
    response = await ac.post('/company/100/ownership', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company not found'


async def test_give_ownership_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 3
    }
    response = await ac.post('/company/2/ownership', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_give_ownership_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 100
    }
    response = await ac.post('/company/2/ownership', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_give_ownership_user_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 4
    }
    response = await ac.post('/company/2/ownership', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not admin"


async def test_give_ownership_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 4
    }
    response = await ac.post('/company/1/ownership', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("users")[0].get("membership_company_id") == 1
    assert response.json().get('result').get("users")[0].get("membership_user_id") == 4
    assert response.json().get('result').get("users")[0].get("membership_role") == "owner"
    assert response.json().get('result').get("users")[1].get("membership_user_id") == 1
    assert response.json().get('result').get("users")[1].get("membership_role") == "admin"


async def test_get_company_by_id(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/company/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("company_id") == 1
    assert response.json().get("result").get("company_owner_id") == 4