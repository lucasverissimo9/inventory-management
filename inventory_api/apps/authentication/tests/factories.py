import factory
from apps.users.models import User
from apps.company.models import Company, CompanyUserMembership

class UserFactory(factory.django.DjangoModelFactory):

    email = factory.Sequence(lambda n: f"{n}@test.com")
    name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    class Meta:
        model = User


class CompanyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")

    company_data = {
        "email": "johndoe@test.com",
        "address": {
            "street": "5th Avenue",
            "city": "New York",
            "postal_code": "10028",
            "country": "EUA"
        }
    }

    status = "active"

    class Meta:
        model = Company

class CompanyUserMembershipFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    user_role = CompanyUserMembership.UserRole.MEMBER

    class Meta:
        model = CompanyUserMembership