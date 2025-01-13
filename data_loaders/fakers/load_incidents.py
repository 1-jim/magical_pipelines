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

    num_records = int(kwargs['records'])

    # Define date range
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 1, 1)

    fake = Faker('en_GB')

    data = []
    for _ in range(num_records):
        incident_type = random.choice(['Accident', 'Injury', 'Property Damage', 'Equipment Failure', 'Environmental Incident', 
                                       'Security Breach', 'Near Miss', 'Workplace Violence', 'Health and Safety Violation'])
        description = fake.text()
        incident_date_datetype = fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=None)
        incident_date = str(incident_date_datetype)
        hours_into_shift = random.randint(0, 23)
        affected_person_name = fake.name()
        site_id = random.randint(1, 12)  # Assuming 12 sites
        severity_level = random.choice(['Low', 'Medium', 'High'])
        department_involved = random.choice(['Operations', 'Human Resources', 'IT', 'Safety', 'Security', 'Legal', 'Finance'])
        incident_status = random.choice(['Open', 'Closed', 'In Progress'])
        root_cause = fake.sentence()
        corrective_actions = fake.paragraph()
        preventive_actions = fake.paragraph()
        investigation_notes = fake.paragraph()
        reported_by = fake.name()
        assigned_to = fake.name()
        resolution_date = str(fake.date_time_between(start_date=incident_date_datetype, end_date=end_date, tzinfo=None))
        resolution_notes = fake.paragraph() if resolution_date else None
        follow_up_required = random.choice([True, False])
        follow_up_date = str(fake.date_time_between(start_date=incident_date_datetype, end_date=end_date, tzinfo=None))
        
        incident = {
            'incident_type': incident_type,
            'description': description,
            'incident_date': incident_date,
            'hours_into_shift': hours_into_shift,
            'affected_person_name': affected_person_name,
            'site_id': site_id,
            'severity_level': severity_level,
            'department_involved': department_involved,
            'incident_status': incident_status,
            'root_cause': root_cause,
            'corrective_actions': corrective_actions,
            'preventive_actions': preventive_actions,
            'investigation_notes': investigation_notes,
            'reported_by': reported_by,
            'assigned_to': assigned_to,
            'resolution_date': resolution_date,
            'resolution_notes': resolution_notes,
            'follow_up_required': follow_up_required,
            'follow_up_date': follow_up_date
        }
        data.append(incident)
    return pd.DataFrame(data)