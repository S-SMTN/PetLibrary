from django.http import HttpResponse, HttpRequest

from Borrowings.factories import BorrowingFactory


def factory_borrowing(request: HttpRequest):
    tenant = request.tenant

    borrowings = BorrowingFactory.create_batch(10, tenant=tenant)

    return HttpResponse(f"{[str(borrowing) for borrowing in borrowings]}")
