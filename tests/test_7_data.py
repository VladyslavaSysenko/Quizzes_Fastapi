from httpx import AsyncClient


# GET ALL USERS COMPANY JSON DATA


async def test_get_company_users_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/company/2/quizzes')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_users_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/quizzes', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_users_data_json_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_users_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/js/company/2/quizzes', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_company_users_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# GET ONE USER COMPANY JSON DATA


async def test_get_company_user_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/company/2/quizzes/member/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_user_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/quizzes/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_user_data_json_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_user_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/js/company/2/quizzes/member/2', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_company_user_data_json_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes/member/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_company_user_data_json_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes/member/6', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not a member of this company"


async def test_get_company_user_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quizzes/member/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# GET ALL USERS QUIZ JSON DATA


async def test_get_quiz_users_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/company/2/quiz/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_quiz_users_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/quiz/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_quiz_users_data_json_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_quiz_users_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/jso/company/2/quiz/2', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_quiz_users_data_json_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_quiz_users_data_json_quiz_not_companys(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/5', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_quiz_users_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/3', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# GET ONE USER QUIZ JSON DATA


async def test_get_quiz_users_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/company/2/quiz/2/member/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_quiz_users_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/quiz/2/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_quiz_users_data_json_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_quiz_users_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/jso/company/2/quiz/2/member/2', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_quiz_users_data_json_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/100/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_quiz_users_data_json_quiz_not_companys(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/5/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_quiz_user_data_json_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2/member/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_quiz_user_data_json_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2/member/6', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not a member of this company"


async def test_get_quiz_users_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/3/member/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# GET MY ALL JSON DATA


async def test_get_my_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/js/my', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_my_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


#GET MY COMPANY JSON DATA


async def test_get_my_company_data_json_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/data/json/company/2/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_company_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/js/company/2/my', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_my_company_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_my_company_data_json_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_my_company_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/json/company/2/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


#GET MY QUIZ JSON DATA


async def test_get_my_quiz_data_json_not_auth(ac: AsyncClient):
    response = await ac.get('/data/json/company/2/quiz/2/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_quiz_data_json_incorrect_type(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/js/company/2/quiz/2/my', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Data type can only be json or csv"


async def test_get_my_quiz_data_json_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/100/quiz/2/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_my_quiz_data_json_user_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_my_quiz_data_json_quiz_not_found(ac: AsyncClient, users_tokens): 
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/100/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_my_quiz_data_json_quiz_not_companys(ac: AsyncClient, users_tokens): 
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/5/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_my_quiz_data_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/json/company/2/quiz/2/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


#-----------------------------------------------------------------------------
# GET CSV DATA


async def test_get_company_users_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/quizzes', headers=headers)
    assert response.status_code == 200


async def test_get_company_user_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/quizzes/member/1', headers=headers)
    assert response.status_code == 200


async def test_get_quiz_users_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/quiz/3', headers=headers)
    assert response.status_code == 200
    

async def test_get_quiz_user_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/quiz/3/member/1', headers=headers)
    assert response.status_code == 200


async def test_get_my_data_csv_success(ac: AsyncClient, users_tokens): 
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/csv/my', headers=headers)
    assert response.status_code == 200


async def test_get_my_company_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/my', headers=headers)
    assert response.status_code == 200


async def test_get_my_quiz_data_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/csv/company/2/quiz/3/my', headers=headers)
    assert response.status_code == 200