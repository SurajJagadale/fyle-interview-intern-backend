import pytest
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.decorators import AuthPrincipal

@pytest.fixture
def assignment():
    return Assignment(id=1, student_id=1, teacher_id=1, content='Test content', state=AssignmentStateEnum.DRAFT)

@pytest.fixture
def auth_principal():
    return AuthPrincipal(student_id=1, teacher_id=1, principal_id=1)

def test_is_graded(assignment):
    assignment.state = AssignmentStateEnum.GRADED
    assert assignment.is_graded()

def test_is_submitted(assignment):
    assignment.state = AssignmentStateEnum.SUBMITTED
    assert assignment.is_submitted()

def test_is_draft(assignment):
    assignment.state = AssignmentStateEnum.DRAFT
    assert assignment.is_draft()