from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest):
    tenant = request.tenant
    domain = tenant.domain_url
    host = request.get_host()
    return HttpResponse((
        f"<h1>Tenant: {tenant}</h1>",
        f"<h1>Domain: {domain}</h1>",
        f"<h1>Host: {host}</h1>",
        f"<h1>Welcome to public!</h1>"
    ))
