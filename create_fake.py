from faker import Faker
import random
from decimal import Decimal
from patient_data.models import S1ParentMain, City
from django.contrib.auth.models import User

fake = Faker()


def generate_crnumber(length=6):
    while True:
        crnumber = str(fake.random_number(digits=length, fix_len=True))
        if not S1ParentMain.objects.filter(crnumber=crnumber).exists():
            return crnumber


def random_age():
    return random.randint(18, 100)


def random_height():
    return random.randint(40, 250)


def random_weight():
    return random.randint(40, 150)


def random_gender():
    return random.choice(['Male', 'Female'])


def random_ecog():
    return random.choice(['Fully active, able to carry on all pre-disease performance without restriction',
                          'Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work',
                          'Ambulatory and capable of all selfcare but unable to carry out any work activities; up and about more than 50% of waking hours',
                          'Capable of only limited selfcare; confined to bed or chair more than 50% of waking hours',
                          'Completely disabled; cannot carry on any selfcare; totally confined to bed or chair',
                          'Dead'])


def random_docid():
    return random.choice(['abcd1234', 'a1b2c3d4', 'b2n3c4j5', 'd3g4h3', 'k3jj45'])


def random_doctype():
    return random.choice(['Aadhar', 'PAN', 'Passport', 'Passport', 'Voter ID', 'Other'])


def random_smoker():
    return random.choice(['Yes', 'No'])


def random_smoking_status():
    return random.choice(['', '<5 years', '>5 & <=10 years','>10 & <=20 years','>20 & <=30 years', '>30 & <=40 years',
                          '>40 & <=50 years', '>50 years'])


def random_smoking_volume():
    return random.choice(['', '<=1 pack/day', '>1 pack <=2 pack', '>1 pack <=2 pack', '>2 pack <=3 pack',
                          '>3 pack <=4 pack','>4 pack <=5 pack','>5 pack'])


def random_user():
    all_user = []
    users = User.objects.all()
    for user in users:
        all_user.append(user)
    return random.choice(all_user)


def random_city():
    all_city = []
    cities = City.objects.all()
    for city in cities:
        all_city.append(city)
    return random.choice(all_city)


def random_updated_by():
    return random.choice(['kundan25', 'testuser'])


def create_reg(n=100):
    data = []
    for _ in range(n):
        data.append(
            S1ParentMain(
                crnumber=generate_crnumber(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                age=random_age(),
                weight=random_weight(),
                height=random_height(),
                reg_date=fake.date_time(),
                gender=random_gender(),
                ecog=fake.paragraph(),
                doc_type=random_doctype(),
                doc_id=random_docid(),
                city=random_city(),
                smoking=random_smoker(),
                smoking_status=random_smoking_status(),
                smoking_volume=random_smoking_volume(),
                email=fake.email(),
                mobile=fake.random_number(digits=10, fix_len=True),
                notes=fake.paragraph(),
                user=random_user(),
                updated_by=random_updated_by()
            )
        )
    return data
