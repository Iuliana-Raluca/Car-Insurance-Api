import factory
from faker import Faker
from owners.models import Owner
from cars.models import Car
from insurance.models import InsurancePolicy
from claims.models import Claim

fake = Faker()

class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Owner
    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())

class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car
    vin = factory.LazyAttribute(lambda _: fake.unique.bothify(text="?????????????????"))  # 17 chars random
    make = "VW"
    model = "Golf"
    year_of_manufacture = 2018
    owner = factory.SubFactory(OwnerFactory)

class PolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsurancePolicy
    car = factory.SubFactory(CarFactory)
    provider = "ACME"
    start_date = factory.Faker("date_object")
    end_date = factory.Faker("date_object")

class ClaimFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Claim
    car = factory.SubFactory(CarFactory)
    claim_date = factory.Faker("date_object")
    description = factory.LazyAttribute(lambda _: fake.sentence())
    amount = "100.00"
