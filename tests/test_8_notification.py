from httpx import AsyncClient


# GET ALL NOTIFICATIONS


async def test_get_all_notifications_not_auth(ac: AsyncClient):
    response = await ac.get('/notifications')
    assert response.status_code == 403


async def test_get_all_notifications_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/notifications', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"
    assert len(response.json().get('result').get('notifications')) == 2


# GET NOTIFICATION


async def test_get_notification_not_auth(ac: AsyncClient):
    response = await ac.get('/notification/1')
    assert response.status_code == 403


async def test_get_notification_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/notification/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Notification not found"


async def test_get_notification_not_users(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/notification/5', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your notification"


async def test_get_notification_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/notification/4', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"
    assert response.json().get('result').get("notification_id") == 4
    assert response.json().get('result').get("notification_user_id") == 2
    assert response.json().get('result').get("notification_quiz_id") == 2
    assert response.json().get('result').get("notification_company_id") == 2
    assert response.json().get('result').get("notification_text") == 'New quiz "quiz_2" has been created'
    assert response.json().get('result').get("notification_status") == False


# CHANGE STATUS


async def test_change_status_not_auth(ac: AsyncClient):
    response = await ac.post('/notification/1/status')
    assert response.status_code == 403


async def test_change_status_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/notification/100/status', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Notification not found"


async def test_change_status_not_users(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/notification/5/status', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your notification"


async def test_change_status_to_read_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/notification/4/status', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"
    assert response.json().get('result').get("notification_status") == True


async def test_change_status_to_unread_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/notification/4/status', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"
    assert response.json().get('result').get("notification_status") == False


# DELETE NOTIFICATION


async def test_delete_notification_not_auth(ac: AsyncClient):
    response = await ac.delete('/notification/1')
    assert response.status_code == 403


async def test_delete_notification_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/notification/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Notification not found"


async def test_delete_notification_not_users(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/notification/5', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your notification"


async def test_delete_notification_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/notification/4', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"
