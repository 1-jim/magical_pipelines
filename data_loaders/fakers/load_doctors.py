import io
import pandas as pd
from faker import Faker
from datetime import datetime
import json
import random
from datetime import datetime, timedelta
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_faker(*args, **kwargs):

    doctor_count = int(kwargs['doctors'])
    
    fake = Faker(['en-GB'])
    Faker.seed(42)
    # Define date range for dob
    start_date = datetime(1920, 1, 1)
    end_date = datetime(2000, 1, 1)

    # create custom ethnicity options
    from faker.providers import BaseProvider
    # create new provider class
    class MyNhsProvider(BaseProvider):

        def nhsSpecialisation(self) -> str:
            SPECIALTYOPTIONS=["Surgery", "General Practice (GP)", "Community Health", "Medicine"]
            return self.random_elements(SPECIALTYOPTIONS, length=1)[0]

        def nhsEthnicity(self) -> str:
            ETHNICITYOPTIONS=["Asian, Asian British, Asian Welsh", "Black, Black British, Black Welsh, Caribbean or African", "Mixed or Multiple", "White", "Other ethnic group"]
            return self.random_elements(ETHNICITYOPTIONS, length=1)[0]
    # then add new provider to faker instance
    fake.add_provider(MyNhsProvider)

    data = []
    for _ in range(doctor_count):
        docM = {
            'DOC_ID': fake.bothify(text='DOC-########'),
            'NAME': fake.name_male(),
            'DOB': fake.date_between_dates(date_start=start_date,date_end=end_date),
            'GENDER': 'Male',
            'ETHNICITY': fake.nhsEthnicity(),
            'OCCUPATION': fake.nhsSpecialisation(),
            'EMAIL': fake.email("fakedomain.nhs"),
            'PHONE_NUMBER': fake.phone_number(),
            'ADDRESS': fake.address(),
            'CITY': fake.city(),
            'EXTRACT_TS': str(datetime.utcnow())
        }
        data.append(docM)
        docF = {
            'DOC_ID': fake.bothify(text='DOC-########'),
            'NAME': fake.name_female(),
            'DOB': fake.date_between_dates(date_start=start_date,date_end=end_date),
            'GENDER': 'Female',
            'ETHNICITY': fake.nhsEthnicity(),
            'OCCUPATION': fake.nhsSpecialisation(),
            'EMAIL': fake.email("fakedomain.nhs"),
            'PHONE_NUMBER': fake.phone_number(),
            'ADDRESS': fake.address(),
            'CITY': fake.city(),
            'EXTRACT_TS': str(datetime.utcnow())
        }
        data.append(docF)

    df = pd.DataFrame(data)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
