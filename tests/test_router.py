from http import HTTPMethod

import pytest
from webob import Request, Response

from web import Router


@pytest.fixture
def router():
    return Router()


def test_get_route(router):
    @router.get("/hello")
    def hello(request):
        return Response("Hello, World!")

    environ = {"PATH_INFO": "/hello", "REQUEST_METHOD": "GET"}
    response = Request(environ).get_response(router)

    assert response.status_code == 200
    assert response.text == "Hello, World!"


def test_post_route(router):
    @router.post("/submit")
    def submit(request):
        return Response("Data submitted!")

    environ = {"PATH_INFO": "/submit", "REQUEST_METHOD": "POST"}
    response = Request(environ).get_response(router)

    assert response.status_code == 200
    assert response.text == "Data submitted!"


def test_not_found_route(router):
    environ = {"PATH_INFO": "/not-found", "REQUEST_METHOD": "GET"}
    response = Request(environ).get_response(router)

    assert response.status_code == 404


def test_custom_not_found_handler(router):

    environ = {"PATH_INFO": "/nonexistent", "REQUEST_METHOD": "GET"}
    response = Request(environ).get_response(router)

    assert response.status_code == 404


def test_exception_handling(router):
    @router.get("/error")
    def error(request):
        raise RuntimeError("Unexpected error")

    environ = {"PATH_INFO": "/error", "REQUEST_METHOD": "GET"}
    response = Request(environ).get_response(router)

    assert response.status_code == 500


def test_route_with_multiple_methods(router):
    @router.routes("/multi", methods=[HTTPMethod.GET, HTTPMethod.POST])
    def multi(request):
        return Response(f"Method used: {request.method}")

    get_environ = {"PATH_INFO": "/multi", "REQUEST_METHOD": "GET"}
    post_environ = {"PATH_INFO": "/multi", "REQUEST_METHOD": "POST"}

    get_response = Request(get_environ).get_response(router)
    post_response = Request(post_environ).get_response(router)

    assert get_response.status_code == 200
    assert get_response.text == "Method used: GET"
    assert post_response.status_code == 200
    assert post_response.text == "Method used: POST"
