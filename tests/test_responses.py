import unittest
import tempfile
import os

from jinja2.exceptions import TemplateNotFound

from web.responses import JsonResponse, HTMLResponse, ContentType


class TestJsonResponse(unittest.TestCase):
    def test_json_response_body(self):
        body = {"success": True, "message": "Hello, World!"}
        response = JsonResponse(body=body)

        self.assertEqual(response.content_type, ContentType.JSON.value)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body.decode('utf-8'), '{"success":true,"message":"Hello, World!"}')

    def test_empty_json(self):
        body = {}
        response = JsonResponse(body=body)

        self.assertEqual(response.content_type, ContentType.JSON.value)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body.decode('utf-8'), '{}')

    def test_another_status(self):
        body = {}
        response = JsonResponse(body=body, status=201)

        self.assertEqual(response.content_type, ContentType.JSON.value)
        self.assertEqual(response.status_code, 201)


class TestHTMLResponse(unittest.TestCase):
    def setUp(self):
        self.template_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        self._write_to_file("<h1>Hello, {{ name }}!</h1>")

    def tearDown(self):
        if os.path.exists(self.template_file.name):
            os.remove(self.template_file.name)

    def _write_to_file(self, txt: str):
        with open(self.template_file.name, mode='w', encoding='utf8') as file:
            file.write(txt)

    def test_html_response_with_jinja(self):
        context = {"name": "Test"}
        response = HTMLResponse(
            template_path=os.path.basename(self.template_file.name),
            context=context,
            templates_dir=os.path.dirname(self.template_file.name)
        )
        self.assertEqual(response.content_type, ContentType.HTML.value)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("<h1>Hello, Test!</h1>", response.body.decode('utf-8'))

        context = {}
        response = HTMLResponse(
            template_path=os.path.basename(self.template_file.name),
            context=context,
            templates_dir=os.path.dirname(self.template_file.name)
        )
        self.assertEqual(response.content_type, ContentType.HTML.value)
        self.assertEqual("<h1>Hello, !</h1>", response.body.decode('utf-8'))

    def test_html_response_without_jinja(self):
        self._write_to_file("<h1>Hello!</h1>")
        response = HTMLResponse(
            template_path=os.path.basename(self.template_file.name),
            context={},
            templates_dir=os.path.dirname(self.template_file.name)
        )
        self.assertEqual(response.content_type, ContentType.HTML.value)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body.decode('utf-8'), "<h1>Hello!</h1>")

        self._write_to_file("")
        response = HTMLResponse(
            template_path=os.path.basename(self.template_file.name),
            context={},
            templates_dir=os.path.dirname(self.template_file.name)
        )
        self.assertEqual(response.content_type, ContentType.HTML.value)
        self.assertEqual(response.body.decode('utf-8'), "")

    def test_another_status(self):
        response = HTMLResponse(
            template_path=os.path.basename(self.template_file.name),
            context={},
            templates_dir=os.path.dirname(self.template_file.name),
            status=201
        )
        self.assertEqual(response.content_type, ContentType.HTML.value)
        self.assertEqual(response.status_code, 201)

    def test_html_response_invalid_template(self):
        with self.assertRaises(TemplateNotFound):
            HTMLResponse(
                template_path="nonexistent_template.html",
                context={},
                templates_dir=os.path.dirname(self.template_file.name)
            )
