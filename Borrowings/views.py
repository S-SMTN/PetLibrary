from django.http import HttpResponse

from Borrowings.factories import BorrowingFactory


def factory_borrowing(request):
    borrowings = BorrowingFactory.create_batch(10)

    return HttpResponse(f"{[str(borrowing) for borrowing in borrowings]}")
