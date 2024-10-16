from django.http import HttpResponse, HttpRequest
from django.db import connection


def index(request: HttpRequest):
    tenant = connection.tenant
    domain = tenant.domain_url
    host = request.get_host()
    return HttpResponse((
        f"<h1>Tenant: {tenant}</h1>",
        f"<h1>Domain: {domain}</h1>",
        f"<h1>Host: {host}</h1>",
        f"<h1>We are privat</h1>",
        f"<h1>User: {request.user}</h1>"
    ))
