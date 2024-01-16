import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum
from core import db

@pytest.fixture
def transactional_session(request):
    """
    Fixture to start a transaction before a test and rollback after the test.
    """
    db.session.begin(subtransactions=True)
    request.addfinalizer(db.session.rollback)

def test_get_assignments(client, h_principal):
    response = client.get(
            '/principal/assignments',
            headers=h_principal
        )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]
        
def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 2,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

@pytest.mark.usefixtures("transactional_session")
def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C

@pytest.mark.usefixtures("transactional_session")
def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B