from httpx import AsyncClient


# CREATE QUIZ

async def test_create_quiz_not_auth(ac: AsyncClient):
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', json=payload)
    assert response.status_code == 403


async def test_create_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/100/quiz', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_create_quiz_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_create_quiz_no_quiz_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "String cannot be empty"


async def test_create_quiz_not_two_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Quiz must have at least two questions"


async def test_create_quiz_no_question_text(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "String cannot be empty"


async def test_create_quiz_same_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Questions must be different"
    


async def test_create_quiz_not_two_choices(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Question must have at least two answer choices"


async def test_create_quiz_same_choices(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_1"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Answer choices must be different"


async def test_create_quiz_no_correct_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_3"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Correct answer must be in answer choices"


async def test_create_quiz_owner_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get("result").get("quiz_name") == "string"
    assert response.json().get("result").get("quiz_description") == "string"
    assert response.json().get("result").get("quiz_frequency_in_days") == 1
    assert response.json().get("result").get("quiz_id") == 1
    assert response.json().get("result").get("quiz_questions") == [
            {
            "question_text": "question_1",
            "question_id": 1,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_2",
            "question_id": 2,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }
        ]

async def test_create_quiz_admin_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_2",
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.post('/company/2/quiz', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get("result").get("quiz_name") == "string"
    assert response.json().get("result").get("quiz_description") == "string"
    assert response.json().get("result").get("quiz_frequency_in_days") == 1
    assert response.json().get("result").get("quiz_id") == 2
    assert response.json().get("result").get("quiz_questions") == [
            {
            "question_text": "question_1",
            "question_id": 3,
            "question_quiz_id": 2,
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_id": 4,
            "question_quiz_id": 2,
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]


# GET ALL QUIZZES


async def test_get_quizzes_not_auth(ac: AsyncClient):
    response = await ac.get('/company/2/quizzes')
    assert response.status_code == 403


async def test_get_quizzes_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/100/quizzes', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_get_quizzes_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/2/quizzes', headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "You are not a member of this company"


async def test_get_quizzes_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/2/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 2


# UPDATE QUIZ


async def test_update_quiz_not_auth(ac: AsyncClient):
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', json=payload)
    assert response.status_code == 403


async def test_update_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/100/quiz/1', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company not found"


async def test_update_quiz_not_owner_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_update_quiz_no_quiz_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "String cannot be empty"


async def test_update_quiz_not_two_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Quiz must have at least two questions"


async def test_update_quiz_no_question_text(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "String cannot be empty"


async def test_update_quiz_same_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Questions must be different"
    


async def test_update_quiz_not_two_choices(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Question must have at least two answer choices"


async def test_update_quiz_same_choices(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_1"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Answer choices must be different"


async def test_update_quiz_no_correct_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_3"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Correct answer must be in answer choices"


async def test_update_quiz_info_owner_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "string",
        "quiz_description": "NEW"
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get("result").get("quiz_name") == "string"
    assert response.json().get("result").get("quiz_description") == "NEW"
    assert response.json().get("result").get("quiz_frequency_in_days") == 1
    assert response.json().get("result").get("quiz_id") == 1
    assert response.json().get("result").get("quiz_questions") == [
            {
            "question_text": "question_1",
            "question_id": 1,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_2",
            "question_id": 2,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }
        ]


async def test_update_quiz_questions_admin_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_questions": [
            {
            "question_text": "question_NEW",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }, {
            "question_text": "question_2",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get("result").get("quiz_name") == "string"
    assert response.json().get("result").get("quiz_description") == "NEW"
    assert response.json().get("result").get("quiz_frequency_in_days") == 1
    assert response.json().get("result").get("quiz_id") == 1
    assert response.json().get("result").get("quiz_questions") == [
            {
            "question_text": "question_NEW",
            "question_id": 5,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }, 
            {
            "question_text": "question_2",
            "question_id": 6,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }
        ]

async def test_update_full_quiz_admin_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "new_name",
        "quiz_description": "string",
        "quiz_frequency_in_days": 1,
        "quiz_questions": [
            {
            "question_text": "question_1",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_2"
            }, {
            "question_text": "question_NEW",
            "question_choices": [
                "choice_1", "choice_2"
            ],
            "question_answer": "choice_1"
            }
        ]
    }
    response = await ac.put('/company/2/quiz/1', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get("result").get("quiz_name") == "new_name"
    assert response.json().get("result").get("quiz_description") == "string"
    assert response.json().get("result").get("quiz_frequency_in_days") == 1
    assert response.json().get("result").get("quiz_id") == 1
    assert response.json().get("result").get("quiz_questions") == [
            {
            "question_text": "question_1",
            "question_id": 7,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_2"
            }, 
            {
            "question_text": "question_NEW",
            "question_id": 8,
            "question_quiz_id": 1,
            "question_choices": ["choice_1", "choice_2"],
            "question_answer": "choice_1"
            }
        ]


# DELETE QUIZ

async def test_quiz_delete_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/2/quiz/1')
    assert response.status_code == 403


async def test_quiz_delete_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/quiz/1', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company not found'


async def test_quiz_delete_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/2/quiz/1', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You don't have permission"


async def test_quiz_delete_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/2/quiz/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


async def test_quiz_delete_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/company/2/quiz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_quiz_list_success_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/2/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 1