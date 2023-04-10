from httpx import AsyncClient
from datetime import date


# GET COMPANY USERS ANALYTICS FOR ALL TIME


async def test_get_company_users_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/members')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_users_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/members', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_users_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/members', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_users_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/members', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("analytics")[0].get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("company_result") == 1.0
    assert response.json().get('result').get("analytics")[0].get("analytics")[1].get("company_result") == 0.75
    assert response.json().get('result').get("analytics")[0].get("analytics")[2].get("company_result") == 0.83
    assert response.json().get('result').get("analytics")[1].get("user_id") == 2
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("company_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("company_result") == 0.25


# GET COMPANY USER ANALYTICS FOR ALL TIME


async def test_get_company_user_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/member/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_user_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_user_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_user_analytics_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/member/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_company_user_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/member/6', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not a member of this company"


async def test_get_company_user_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/member/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("user_id") == 2
    assert response.json().get('result').get("analytics")[0].get("company_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("company_result") == 0.25
    
    
# # GET COMPANY QUIZZES USERS ANALYTICS FOR ALL TIME


async def test_get_company_quizzes_users_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quizzes/members')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_quizzes_users_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quizzes/members', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_quizzes_users_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/members', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_quizzes_users_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/members', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("analytics")[0].get("quiz_id") == 2
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("analytics")[0].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("analytics")[0].get("quiz_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("quiz_id") == 3
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("user_id") == 1
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("analytics")[1].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("analytics")[1].get("quiz_result") == 0.75
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("user_id") == 2
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("analytics")[0].get("record_result") == 0.0
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("analytics")[0].get("quiz_result") == 0.0
    assert response.json().get('result').get("analytics")[2].get("quiz_id") == 4
    assert response.json().get('result').get("analytics")[2].get("analytics")[0].get("user_id") == 2
    assert response.json().get('result').get("analytics")[2].get("analytics")[0].get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[2].get("analytics")[0].get("analytics")[0].get("quiz_result") == 0.5
    

# GET COMPANY QUIZZES USER ANALYTICS FOR ALL TIME


async def test_get_company_quizzes_user_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quizzes/member/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_company_quizzes_user_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quizzes/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_company_quizzes_user_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_company_quizzes_user_analytics_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/member/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_company_quizzes_user_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/member/6', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not a member of this company"


async def test_get_company_quizzes_user_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/member/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("user_id") == 2
    assert response.json().get('result').get("analytics")[0].get("quiz_id") == 3
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("record_result") == 0.0
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("quiz_result") == 0.0
    assert response.json().get('result').get("analytics")[1].get("quiz_id") == 4
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("quiz_result") == 0.5
    

# GET QUIZ USERS ANALYTICS FOR ALL TIME


async def test_get_quiz_users_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quiz/2/members')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_quiz_users_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quiz/2/members', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_quiz_users_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/2/members', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_quiz_users_analytics_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/100/members', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_quiz_users_analytics_quiz_not_companys(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/5/members', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_quiz_users_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/3/members', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("quiz_id") == 3
    assert response.json().get('result').get("analytics")[0].get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result').get("analytics")[0].get("analytics")[1].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[0].get("analytics")[1].get("quiz_result") == 0.75
    assert response.json().get('result').get("analytics")[1].get("user_id") == 2
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("record_result") == 0.0
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("quiz_result") == 0.0


# GET QUIZ USER ANALYTICS FOR ALL TIME


async def test_get_quiz_user_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quiz/2/member/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_quiz_user_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quiz/2/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_quiz_user_analytics_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/2/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_quiz_user_analytics_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/100/member/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_quiz_user_analytics_quiz_not_companys(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/5/member/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_quiz_user_analytics_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/2/member/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_quiz_user_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/2/member/6', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User is not a member of this company"


async def test_get_quiz_user_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/3/member/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("quiz_id") == 3
    assert response.json().get('result').get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("quiz_result") == 0.75


# GET USERS LAST COMPANY RECORD TIME


async def test_get_users_last_company_record_time_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/last/company/2/members')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_users_last_company_record_time_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/last/company/100/members', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_users_last_company_record_timenot_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/last/company/2/members', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_get_users_last_company_record_time_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/last/company/2/members', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("analytics")[0].get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("date") == str(date.today())
    assert response.json().get('result').get("analytics")[1].get("user_id") == 2
    assert response.json().get('result').get("analytics")[1].get("date") == str(date.today())
    assert response.json().get('result').get("analytics")[2].get("user_id") == 3
    assert response.json().get('result').get("analytics")[2].get("date") == None
    assert response.json().get('result').get("analytics")[3].get("user_id") == 4
    assert response.json().get('result').get("analytics")[3].get("date") == None


# GET USER SYSTEM RESULT


async def test_get_user_system_result_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/user/2')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_user_system_result_user_not_found(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/user/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "User not found"


async def test_get_user_system_result_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/user/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("user_id") == 2
    assert response.json().get('result').get("system_result") == 0.25


# GET MY COMPANIES ANALYTICS FOR ALL TIME


async def test_get_my_companies_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/companies/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_companies_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/companies/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result')[0].get("company_id") == 1
    assert response.json().get('result')[0].get("analytics")[0].get("company_result") == 0.0
    assert response.json().get('result')[1].get("company_id") == 2
    assert response.json().get('result')[1].get("analytics")[0].get("company_result") == 1.0
    assert response.json().get('result')[1].get("analytics")[1].get("company_result") == 0.75
    assert response.json().get('result')[1].get("analytics")[2].get("company_result") == 0.83


# GET MY QUIZZES ANALYTICS FOR ALL TIME


async def test_get_my_quizzes_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/companies/quizzes/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_quizzes_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/companies/quizzes/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result')[0].get("company_id") == 1
    assert response.json().get('result')[0].get("analytics")[0].get("quiz_id") == 5
    assert response.json().get('result')[0].get("analytics")[0].get("analytics")[0].get("quiz_result") == 0.0
    assert response.json().get('result')[1].get("company_id") == 2
    assert response.json().get('result')[1].get("analytics")[0].get("quiz_id") == 2
    assert response.json().get('result')[1].get("analytics")[0].get("analytics")[0].get("quiz_result") == 1.0
    assert response.json().get('result')[1].get("analytics")[1].get("quiz_id") == 3
    assert response.json().get('result')[1].get("analytics")[1].get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result')[1].get("analytics")[1].get("analytics")[1].get("quiz_result") == 0.75


# GET MY COMPANY COMPANY ANALYTICS FOR ALL TIME


async def test_get_my_company_company_analytics_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/analytics/company/2/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_company_company_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_my_company_company_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_my_company_company_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/company/2/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("company_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("company_result") == 0.75
    assert response.json().get('result').get("analytics")[2].get("company_result") == 0.83


# GET MY COMPANY QUIZZES ANALYTICS FOR ALL TIME


async def test_get_my_company_quizzes_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quizzes/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_company_quizzes_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quizzes/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_my_company_quizzes_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_my_company_quizzes_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quizzes/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("quiz_id") == 2
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[0].get("analytics")[0].get("quiz_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("quiz_id") == 3
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("analytics")[1].get("quiz_result") == 0.75


# GET MY QUIZ ANALYTICS FOR ALL TIME


async def test_get_my_quiz_analytics_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/quiz/2/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_quiz_analytics_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/quiz/2/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_my_quiz_analytics_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/100/my', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_get_my_quiz_analytics_quiz_not_companys(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/5/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company's quiz"


async def test_get_my_quiz_analytics_user_not_member(ac: AsyncClient, users_tokens):  
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/2/my', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_my_quiz_analytics_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/company/2/quiz/3/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("quiz_id") == 3
    assert response.json().get('result').get("user_id") == 1
    assert response.json().get('result').get("analytics")[0].get("record_result") == 0.5
    assert response.json().get('result').get("analytics")[0].get("quiz_result") == 0.5
    assert response.json().get('result').get("analytics")[1].get("record_result") == 1.0
    assert response.json().get('result').get("analytics")[1].get("quiz_result") == 0.75


# GET MY LAST QUIZZES RECORD TIME


async def test_get_my_last_quizzes_record_time_not_auth(ac: AsyncClient):
    response = await ac.get('/analytics/last/my')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_last_quizzes_record_time_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/analytics/last/my', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result')[0].get("company_id") == 1
    assert response.json().get('result')[0].get("last_records")[0].get("quiz_id") == 5
    assert response.json().get('result')[0].get("last_records")[0].get("date") == str(date.today())
    assert response.json().get('result')[1].get("company_id") == 2
    assert response.json().get('result')[1].get("last_records")[0].get("quiz_id") == 2
    assert response.json().get('result')[1].get("last_records")[0].get("date") == str(date.today())
    assert response.json().get('result')[1].get("last_records")[1].get("quiz_id") == 3
    assert response.json().get('result')[1].get("last_records")[1].get("date") == str(date.today())