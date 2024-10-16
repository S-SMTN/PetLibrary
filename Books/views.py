from django.http import HttpResponse

from Books.factories import BookFactory


def factory_book(request):
    tenant = request.tenant

    books = [BookFactory() for _ in range(10)]

    return HttpResponse(f"{[str(book) for book in books]}")
