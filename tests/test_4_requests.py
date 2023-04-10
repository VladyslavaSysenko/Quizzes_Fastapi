from httpx import AsyncClient

# send request

async def test_send_request_not_auth(ac: AsyncClient):
    payload = {
        "request_to_company_id": 0,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_send_request_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "request_to_company_id": 100,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company not found'


async def test_send_request_from_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "request_to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is already a member of the company"


async def test_send_request_already_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "request_to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is already a member of the company"


async def test_send_request_invite_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "request_to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "Company already sent an invite"


async def test_send_request_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "request_to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_send_invite_request_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "invite_to_user_id": 4,
        "invite_from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User already sent a request"


async def test_send_request_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "request_to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_send_request_already_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "request_to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "Request already sent"


async def test_send_request_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "request_to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# my requests

async def test_my_requests_not_auth(ac: AsyncClient):
    response = await ac.get("/request/my")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_my_requests_user_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0


async def test_my_requests_user_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 1


async def test_my_requests_user_four(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 2


# company requests

async def test_company_requests_not_auth(ac: AsyncClient):
    response = await ac.get("/request/company/1")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_requests_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/100", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_requests_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_requests_company_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/company/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('requests')) == 2


# request cancel


async def test_cancel_requests_not_auth(ac: AsyncClient):
    response = await ac.delete("/request/1")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_cancel_requests_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/request/12", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_cancel_requests_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete("/request/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"


async def test_cancel_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete("/request/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# accept request

async def test_accept_requests_not_auth(ac: AsyncClient):
    response = await ac.get("/request/2/accept")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_accept_requests_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/12/accept", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_accept_requests_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/2/accept", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


# decline request


async def test_decline_request_not_auth(ac: AsyncClient):
    response = await ac.get('/request/3/decline')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decline_request_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/request/100/decline', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_decline_request_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/request/2/decline', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_decline_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/request/2/decline', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"



#===============================


async def test_members_only_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 3


async def test_accept_requests(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/3/accept", headers=headers)
    assert response.status_code == 200


async def test_members_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 4


# ===========

async def test_kick_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/company/2/member/3", headers=headers)
    assert response.status_code == 200


async def test_members_after_kick(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 3


async def test_leave_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete("/company/2/leave", headers=headers)
    assert response.status_code == 200


async def test_members_after_leave(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 2


async def test_send_request_four_again_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "request_to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_accept_request_four(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/4/accept", headers=headers)
    assert response.status_code == 200


async def test_send_request_five_again_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "request_to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_accept_request_five(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/5/accept", headers=headers)
    assert response.status_code == 200


async def test_send_request_six_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "request_to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_accept_request_six(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/6/accept", headers=headers)
    assert response.status_code == 200