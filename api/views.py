import bleach
import markdown
from django.http import HttpRequest, HttpResponse, JsonResponse

# Create your views here.


def render_markdown(request: HttpRequest) -> HttpResponse:
    """renders given Markdown code to HTML
    !!! TODO

    Args:
        request (HttpRequest): POST request with markdown code
                               as the body.

    Returns: HttpResponse containing HTML content generated
             from given markdown code.

    The given markdown input is sanitised using the bleach module to
    prevent cross site scripting.
    """

    # This is a temporary response as the implementation of this
    # endpoint is not complete and requires major bug fixes
    return JsonResponse(
        {"error": "Endpoint Not Implemented"},
        status=405,
        content_type="application/json",
    )

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid Request Type"},
            status=405,
            content_type="application/json",
        )

    md = request.body.decode()
    html = markdown.markdown(md, extensions=["fenced_code", "sane_lists"])

    allowed__tags = [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "code",
        "pre",
        "ol",
        "li",
        "ul",
        "blockquote",
        "a",
        "img",
        "div",
        "strong",
        "em",
    ]
    allowed_attributes = {}

    sanitised_html = bleach.clean(
        html, tags=allowed__tags, attributes=allowed_attributes
    )

    return HttpResponse(sanitised_html)
