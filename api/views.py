import bleach
import markdown
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

# Create your views here.


@require_POST
def render_markdown(request: HttpRequest) -> HttpResponse:
    """renders given Markdown code to HTML

    Args:
        request (HttpRequest): POST request with markdown code
                               as the body.

    Returns: HttpResponse containing HTML content generated
             from given markdown code.

    The given markdown input is sanitised using the bleach module to
    prevent cross site scripting.
    """

    # TODO

    return HttpResponse("Stub")  # stub
