from http import HTTPStatus

from requests import Response


class ResponseSpecs:
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text

        return confirm

    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text

        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

        return confirm

    @staticmethod
    def request_forbidden():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text

        return confirm

    @staticmethod
    def request_unprocessable_entity():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
                response.text
            )

        return confirm

    @staticmethod
    def request_conflict():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text

        return confirm
