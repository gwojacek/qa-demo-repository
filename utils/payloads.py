from faker import Faker

fake = Faker("pl_PL")


def user_create_payload():
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
    address1 = fake.street_address()
    # address2: same as address1 but with a small tweak (e.g., add apt/lokal info)
    address2 = address1 + f" / {fake.random_int(min=1, max=50)}"
    return {
        "name": fake.user_name(),
        "email": fake.unique.email(),
        "password": fake.password(length=12),
        "title": fake.random_element(["Mr", "Mrs", "Miss"]),
        "birth_date": birth_date.day,
        "birth_month": birth_date.month,
        "birth_year": birth_date.year,
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "company": fake.company(),
        "address1": address1,
        "address2": address2,
        "country": "Poland",
        "zipcode": fake.postcode(),
        "state": fake.city(),  # Use city as region if API requires 'state'
        "city": fake.city(),
        "mobile_number": fake.phone_number(),
    }
