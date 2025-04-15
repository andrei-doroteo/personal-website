import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_website.settings")
django.setup()

from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse

# Create your tests here.


class TestRenderMarkdown(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("api:render_markdown")
        self.maxDiff = None

    def make_request(
        self,
        request_type: str,
        body: str | dict,
    ) -> HttpResponse:
        """A helper function to make HttpRequests"""

        match request_type:
            case "post":
                response = self.client.post(
                    self.url, body, content_type="text/plain"
                )
            case "get":
                response = self.client.get(self.url)
            case "head":
                response = self.client.head(self.url)
            case "put":
                response = self.client.put(self.url)
            case "delete":
                response = self.client.delete(self.url)
            case "connect":
                response = self.client.connect(self.url)
            case "options":
                response = self.client.options(self.url)
            case "trace":
                response = self.client.trace(self.url)
            case "patch":
                response = self.client.patch(self.url)

        return response

    def validate_response(
        self,
        response: HttpResponse,
        expected: str = '{"error": "Invalid Request Type"}',
        status_code: int = 405,
        content_type: str = "application/json",
    ) -> None:
        """A helper function to check for expected HttpResponse"""

        self.assertEqual(response.status_code, status_code)
        self.assertTrue(response["Content-Type"].startswith(content_type))
        self.assertEqual(
            expected,
            response.content.decode("utf-8"),
        )

    # test the case of valid markdown content
    # and api successfully returns generated html
    def test_render_markdown_valid(self):

        md = "# Hello World"
        expected = "<h1>Hello World</h1>"

        response = self.make_request("post", body=md)

        self.validate_response(
            response,
            expected=expected,
            status_code=200,
            content_type="text/html",
        )

    # test the case of empty content
    # and api returns empty content
    def test_render_markdown_empty(self):

        md = ""
        expected = ""

        response = self.make_request("post", body=md)

        self.validate_response(
            response,
            expected=expected,
            status_code=200,
            content_type="text/html",
        )

    # test the case of cross site scripting
    # and api returns escaped HTML
    def test_render_markdown_xss(self):

        md = "<script>alert('Injecting Javascript')</script>"
        expected = "&lt;script&gt;alert('Injecting Javascript')&lt;/script&gt;"

        response = self.make_request("post", body=md)

        self.validate_response(
            response,
            expected=expected,
            status_code=200,
            content_type="text/html",
        )

    # test the case of invalid request method
    # (any request other than POST) and api returns an error in JSON
    def test_render_markdown_invalid_request(self):

        def type_of(obj: object):
            return type(obj).__name__

        request_types = [
            "get",
            "put",
            "delete",
            "options",
            "patch",
        ]

        for request_type in request_types:

            body = None

            if type_of(request_type) == "dict":
                request_type = request_type["request_type"]
                body = request_type["body"]

            response = self.make_request(request_type, body)
            print(f"Status: {response.status_code}")
            print(f"Content: {response.content.decode()}")

            self.validate_response(response)

    def test_render_markdown_non_common_request_methods(self):
        # Test HEAD, CONNECT, and TRACE methods
        # "head",
        # "connect",
        # "trace",
        # TODO
        pass

    # test the case of allowed markdown features
    def test_render_markdown_whitelisted_tags(self):

        # !!! Broken Test
        # TODO
        cow_image = (
            "https://cdn.britannica.com/"
            "55/174255-050-526314B6/brown-Guernsey-cow.jpg"
        )

        md = f"""
        # H1
        ## H2
        ### H3
        #### H4
        ##### H5
        ###### H6

        Paragraph Text

        `Inline code block`

        ```python
        # Multiline
            # code
                # block
        ```
        
        1. Numbered
        2. List
        3. Of things

        - Unordered
        - List
        - Of Things

        > Quote

        [Link to google](https://www.google.com)

        [Link to linked-section](#linked-section)

        ![Image of a cow]({cow_image})
        <div id="linked-section">
        More paragraph text
        </div>
        This line has a **bold** word
        This line has an _italic_ word
        """

        expected = """
        <h1>H1</h1>
        <h2>H2</h2>
        <h3>H3</h3>
        <h4>H4</h4>
        <h5>H5</h5>
        <h6>H6</h6>
        <p>Paragraph Text</p>
        <p><code>Inline code block</code></p>
        <pre><code class="language-python"># Multiline
            # code
                # block
        </code></pre>
        <ol>
        <li>Numbered</li>
        <li>List</li>
        <li>Of things</li>
        </ol>
        <ul>
        <li>Unordered</li>
        <li>List</li>
        <li>Of Things</li>
        </ul>
        <blockquote>
        <p>Quote</p>
        </blockquote>
        <p><a href="https://www.google.com">Link to google</a></p>
        <p><a href="#linked-section">Link to linked-section</a></p>
        <p><img alt="Image of a cow" src="https://cdn.britannica.com/55/174255-050-526314B6/brown-Guernsey-cow.jpg" /></p>
        <div id="linked-section">
        More paragraph text
        </div>
        <p>This line has a <strong>bold</strong> word
        This line has an <em>italic</em> word</p>
        """

        response = self.make_request("post", body=md)

        self.validate_response(
            response,
            expected=expected,
            status_code=200,
            content_type="text/html",
        )

    # test the case of disallowed markdown features
    # href attribute script tags, etc...
    def test_render_markdown_non_whitelist(self):
        # TODO
        pass
