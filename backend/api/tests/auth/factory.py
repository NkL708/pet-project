# pylint: disable=too-few-public-methods
import random
import string
from typing import Optional

import factory
from django.contrib.auth.models import User


def generate_complex_password():
    length = random.randint(10, 16)
    choices = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(choices) for _ in range(length))
    return password


class UserFactory(factory.django.DjangoModelFactory):
    # pylint: disable=no-member
    # pylint: disable=attribute-defined-outside-init
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")

    @factory.post_generation
    def post_password(
        self: User, create: bool, extracted: Optional[str]
    ) -> None:
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("StrongP@ssw0rd123")
        self.save()


class UserDictFactory(factory.Factory):
    class Meta:
        model = dict

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(generate_complex_password)
    is_staff = False
