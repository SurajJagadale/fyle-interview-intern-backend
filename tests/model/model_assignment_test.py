from unittest.mock import patch, Mock
from core.models.assignments import Assignment, AssignmentStateEnum

@patch('core.models.assignments.db.session.query')
def test_get_by_id(mock_query):
    mock_assignment = Mock()
    mock_query.return_value.filter.return_value.first.return_value = mock_assignment
    result = Assignment.get_by_id(1)
    assert result == mock_assignment

@patch('core.models.assignments.db.session.query')
@patch('core.models.assignments.db.session.add')
@patch('core.models.assignments.db.session.flush')
def test_upsert_new(mock_flush, mock_add, mock_query):
    mock_assignment = Mock(id=None)
    Assignment.upsert(mock_assignment)
    mock_add.assert_called_once_with(mock_assignment)
    mock_flush.assert_called_once()

@patch('core.models.assignments.db.session.query')
@patch('core.models.assignments.db.session.flush')
def test_upsert_existing(mock_flush, mock_query):
    mock_assignment = Mock(id=1, state=AssignmentStateEnum.DRAFT)
    mock_query.return_value.filter.return_value.first.return_value = mock_assignment
    Assignment.upsert(mock_assignment)
    mock_flush.assert_called_once()

@patch('core.models.assignments.db.session.query')
@patch('core.models.assignments.db.session.flush')
def test_submit(mock_flush, mock_query):
    mock_assignment = Mock(id=1, student_id=1, content='content', state=AssignmentStateEnum.DRAFT)
    mock_query.return_value.filter.return_value.first.return_value = mock_assignment
    mock_principal = Mock(student_id=1)
    Assignment.submit(1, 1, mock_principal)
    assert mock_assignment.state == AssignmentStateEnum.SUBMITTED
    mock_flush.assert_called_once()

# Add more tests for other methods...