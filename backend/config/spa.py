import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound


def spa(request, resource=""):
    """Serve the built React app, and fall back to index.html for client routes."""
    root = Path(settings.FRONTEND_DIST).resolve()
    relative = Path(resource)
    if relative.is_absolute() or ".." in relative.parts:
        return HttpResponseNotFound("Not found.")

    candidate = (root / relative).resolve()
    if root not in candidate.parents and candidate != root:
        return HttpResponseNotFound("Not found.")

    if resource and candidate.is_file():
        content_type, _ = mimetypes.guess_type(candidate.name)
        return FileResponse(candidate.open("rb"), content_type=content_type or "application/octet-stream")

    index = root / "index.html"
    if not index.is_file():
        return HttpResponseNotFound("Frontend build is missing.")
    return FileResponse(index.open("rb"), content_type="text/html")
