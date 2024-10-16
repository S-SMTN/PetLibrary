from django.http import HttpResponse

from Users.factories import UserFactory


def factory_user(request):
    users = UserFactory.create_batch(10)

    return HttpResponse(f"{[str(user) for user in users]}")
