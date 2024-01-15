from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.libs import helpers, assertions

from .schema import AssignmentSchema, AssignmentGradeSchema,TeacherSchema
principal_assignments_resources = Blueprint("principal_assignments_resources",__name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of Graded and Submitted assignments"""
    principal_assignments = Assignment.get_assignments_for_principal()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all the teachers"""
    teacher_list = Teacher.get_all_teachers()
    teacher_list_dump = TeacherSchema().dump(teacher_list, many=True)
    return APIResponse.respond(data=teacher_list_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or Regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    if not Assignment.is_draft(_id=grade_assignment_payload.id):
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )

        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
    
    return APIResponse.respond_error(f"No assignment with ID {grade_assignment_payload.id} was found", status_code=400)