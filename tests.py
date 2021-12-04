from datetime import datetime
from app.database import create_new_pupil, get_all_pupils, get_pupil_data_by_name, activate_day


create_new_pupil(name="Test name", first_name="Test", phone_number="+380059430593")
create_new_pupil(name="Username", first_name="Test2", phone_number="+3843258237834")

pupil_by_name = get_pupil_data_by_name(pupil_name="Username")
print(f"pupil_by_name: {pupil_by_name}\n")

all_pupils = get_all_pupils()

for pupil in all_pupils:
    print(f"name: {pupil}, data: {all_pupils[pupil]}")


date_now = datetime.now()
activate_day(date=date_now)
