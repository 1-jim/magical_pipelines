import io
from datetime import datetime
import pandas as pd

from faker import Faker
fake = Faker()

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def generate_customer_data(num_records):
    data = []
    for _ in range(num_records):
        customer = {
            'customer_id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'address': fake.address(),
            'city': fake.city(),
            'country': fake.country(),
            'EXTRACT_TS': str(datetime.utcnow())
        }
        data.append(customer)
    return data

@data_loader
def load_data(**kwargs):
    customer_list = generate_customer_data(50)
    df = pd.DataFrame(customer_list)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
