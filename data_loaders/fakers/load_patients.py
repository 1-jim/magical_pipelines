import io
import pandas as pd
from faker import Faker
from datetime import datetime
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_faker(df_doctors: DataFrame, *args, **kwargs):

    patient_count = int(int(kwargs['patients'])/2)
    doctor_count = int(kwargs['doctors'])
    
    fake = Faker(['en-GB'])
    Faker.seed(1977)
    # Define date range for dob
    start_date = datetime(1920, 1, 1)
    end_date = datetime(2000, 1, 1)

    # create custom ethnicity options
    from faker.providers import BaseProvider
    # create new provider class
    class MyNhsProvider(BaseProvider):

        def nhsNextAppointment(self) -> str:
            if fake.boolean() == True:
                return ''
            else:
                today = datetime.now()
                future_date = today + timedelta(days=random.randint(1, 365))
                month_name = future_date.strftime("%B").upper()[:3]  # Extract month name and convert to uppercase
                return f"{future_date.day}-{month_name}-{future_date.year}"


        def nhsDependents(self) -> int:
            # 50% chance of having no dependents
            if fake.boolean() == True:
                return 0
            # 50% chance of having 1-3 dependents
            else:
                return random.randint(1, 3)
        
        def nhsJargon(self, num_sentences=5) -> str:
            medical_word_list = [
                "patient", "doctor", "nurse", "hospital", "surgery", "medication", "treatment",
                "diagnosis", "symptom", "disease", "condition", "therapy", "consultation", 
                "prescription", "appointment", "procedure", "examination", "test", "result", 
                "health", "wellness", "emergency", "injury", "recovery", "monitoring", 
                "vaccination", "immunization", "pharmacy", "admission", "discharge", 
                "medication", "dosage", "side effect", "allergy", "infection", "pain", 
                "diagnosis", "therapy", "treatment", "surgery", "rehabilitation", 
                "consultation", "physician", "specialist", "surgeon", "nurse", "therapist", 
                "pharmacist", "medical", "hospital", "clinic", "practice", "emergency room", 
                "operating room", "ward", "ICU", "laboratory", "radiology", "pharmacy", 
                "patient", "healthcare", "insurance", "policy", "coverage", "premium", 
                "claim", "billing", "payment", "benefit", "provider", "coverage", "plan", 
                "formulary", "co-pay", "deductible", "network", "referral", "authorization", 
                "reimbursement", "medical record", "privacy", "HIPAA", "consent", 
                "confidentiality", "ethics", "research", "study", "trial", "protocol", 
                "evidence", "outcome", "researcher", "participant", "volunteer", "informed consent", 
                "placebo", "control group", "experimental group", "blind study", "double-blind study", 
                "peer review", "publication", "conference", "abstract", "poster", "presentation", 
                "journal", "article", "publication", "grant", "funding", "research institution", 
                "university", "college", "researcher", "scientist", "research assistant", "lab technician"
            ]
            sentences = []
            for _ in range(num_sentences):
                sentences.append(fake.sentence(ext_word_list=medical_word_list))
            return ' '.join(sentences)

        def nhsDoctor(self) -> str:
            DROPTS=[]
            for _ in range(doctor_count):
                random_doc = df_doctors.sample(n=1)
                first_doc = random_doc.iloc[0, 0]
                DROPTS.append(first_doc)
            return self.random_elements(DROPTS, length=1)[0]

        def nhsSurgery(self) -> str:
            SURGERYOPTIONS=[]
            for _ in range(10):
                SURGERYOPTIONS.append(fake.street_suffix().upper() + ' Practice')
            return self.random_elements(SURGERYOPTIONS, length=1)[0]

        def nhsEthnicity(self) -> str:
            ETHNICITYOPTIONS=["Asian, Asian British, Asian Welsh", "Black, Black British, Black Welsh, Caribbean or African", "Mixed or Multiple", "White", "Other ethnic group"]
            return self.random_elements(ETHNICITYOPTIONS, length=1)[0]
    # then add new provider to faker instance
    fake.add_provider(MyNhsProvider)

    data = []
    for _ in range(patient_count):
        patientM = {
            'PATIENT_ID': fake.bothify(text='PI-??-########'),
            'NAME': fake.name_male(),
            'DOB': fake.date_between_dates(date_start=start_date,date_end=end_date),
            'GENDER': 'Male',
            'ETHNICITY': fake.nhsEthnicity(),
            'OCCUPATION': fake.job(),
            'EMAIL': fake.email(),
            'PHONE_NUMBER': fake.phone_number(),
            'ADDRESS': fake.address(),
            'CITY': fake.city(),
            'PRESENTING_ISSUES': fake.nhsJargon(num_sentences=5),
            'TREATMENT_GOALS': fake.nhsJargon(num_sentences=2),
            'ASSESSMENT_AND_PROGRESS': fake.nhsJargon(num_sentences=10),
            'DOCTOR_ID': fake.nhsDoctor(),
            'SURGERY_NAME': fake.nhsSurgery(),
            'DEPENDENTS': fake.nhsDependents(),
            'NEXT_APPOINTMENT': fake.nhsNextAppointment(),
            'EXTRACT_TS': str(datetime.utcnow())
        }
        data.append(patientM)
        patientF = {
            'PATIENT_ID': fake.bothify(text='PI-??-########'),
            'NAME': fake.name_female(),
            'DOB': fake.date_between_dates(date_start=start_date,date_end=end_date),
            'GENDER': 'Female',
            'ETHNICITY': fake.nhsEthnicity(),
            'OCCUPATION': fake.job(),
            'EMAIL': fake.email(),
            'PHONE_NUMBER': fake.phone_number(),
            'ADDRESS': fake.address(),
            'CITY': fake.city(),
            'PRESENTING_ISSUES': fake.nhsJargon(num_sentences=5),
            'TREATMENT_GOALS': fake.nhsJargon(num_sentences=2),
            'ASSESSMENT_AND_PROGRESS': fake.nhsJargon(num_sentences=10),
            'DOCTOR_ID': fake.nhsDoctor(),
            'SURGERY_NAME': fake.nhsSurgery(),
            'DEPENDENTS': fake.nhsDependents(),
            'NEXT_APPOINTMENT': fake.nhsNextAppointment(),
            'EXTRACT_TS': str(datetime.utcnow())
        }
        data.append(patientF)

    df = pd.DataFrame(data)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
