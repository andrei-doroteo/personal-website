from django.test import Client, TestCase
from django.urls import reverse

# Create your tests here.


class TestRenderMarkdown(TestCase):

    def setUp(self):
        self.client = Client()

    # test the case of valid markdown content
    # and api successfully returns generated html
    def test_render_markdown_valid(self):

        md = "# Hello World"

        response = self.client.post(
            reverse("api:render_markdown"), data=md, content_type="text/plain"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/html"))
        self.assertEqual(
            "<h1>Hello World</h1>", response.content.decode("utf-8")
        )

    # test the case of empty content
    # and api returns empty content
    def test_render_markdown_empty(self):

        md = ""

        response = self.client.post(
            reverse("api:render_markdown"), data=md, content_type="text/plain"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/html"))
        self.assertEqual("", response.content.decode("utf-8"))

    # test the case of cross site scripting
    # and api returns escaped HTML
    def test_render_markdown_xss(self):

        md = "<script>alert('Injecting Javascript')</script>"

        response = self.client.post(
            reverse("api:render_markdown"), data=md, content_type="text/plain"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/html"))
        self.assertEqual(
            "&lt;script&gt;alert('Injecting Javascript')&lt;/script&gt",
            response.content.decode("utf-8"),
        )

    # test the case of complex valid markdown content
    # including lists, nested elements, code blocks, and tables
    # and api returns successfully generated HTML
    def test_render_markdown_long(self):

        # TODO
        pass

    # test the case of invalid request method (GET, PUT, DELETE, etc...)
    # and api returns an error in JSON
    def test_render_markdown_invalid_req(self):

        md = "# Markdown Text"

        response = self.client.get(
            reverse("api:render_markdown"), data=md, content_type="text/plain"
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(
            response["Content-Type"].startswith("application/json")
        )
        self.assertEqual(
            '{"error":"invalid request type"}',
            response.content.decode("utf-8"),
        )
