import pytest
from unittest.mock import Mock, patch
from core.models.teachers import Teacher
from core.apis.decorators import AuthPrincipal

@pytest.fixture
def teacher():
    return Teacher(id=1, user_id=1)

@pytest.fixture
def auth_principal():
    return AuthPrincipal(user_id=1, teacher_id=1)

def test_filter(teacher):
    with patch('core.models.teachers.db.session.query', return_value=Mock(filter=Mock(return_value=[teacher]))):
        result = Teacher.filter(Teacher.id == 1)
        assert result == [teacher]

def test_get_by_id(teacher):
    with patch('core.models.teachers.Teacher.filter', return_value=Mock(first=Mock(return_value=teacher))):
        result = Teacher.get_by_id(1)
        assert result == teacher

def test_validate(teacher, auth_principal):
    with patch('core.models.teachers.Teacher.get_by_id', return_value=teacher):
        result = Teacher.validate(auth_principal)
        assert result

def test_get_teachers_by_principal(teacher):
    with patch('core.models.teachers.Teacher.filter', return_value=Mock(all=Mock(return_value=[teacher]))):
        result = Teacher.get_teachers_by_principal()
        assert result == [teacher]