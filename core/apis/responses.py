from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))

    @classmethod
    def respond_error(cls, data, status_code=400):
        return make_response(data, status_code)