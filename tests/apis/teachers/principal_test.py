from flask import json

def test_list_teachers(client, h_principal):
    response = client.get('/principal/teachers', headers= h_principal)
    data = json.loads(response.data)
    print(data)
    assert response.status_code == 200
    assert 'data' in data
    assert isinstance(data['data'], list)
    for teacher in data['data']:
        assert 'created_at' in teacher
        assert 'id' in teacher
        assert 'updated_at' in teacher
        assert 'user_id' in teacher