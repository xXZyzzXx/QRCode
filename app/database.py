from uuid import uuid4
import datetime
from typing import Optional, Generator
from json.decoder import JSONDecodeError

from kivy.storage.jsonstore import JsonStore

from app.utils import create_database_folder


create_database_folder()

pupils_store = JsonStore('db/pupils_db.json')
active_days_storage = JsonStore('db/active_days.json')
qr_codes_store = JsonStore('db/qr_codes.json')


# Pupil crud
def create_new_pupil(name: str, first_name: str, phone_number: str) -> bool:
    try:
        pupil_id = str(uuid4().int)[:12]
        pupil_data = {
            "pupil_id": pupil_id,
            "name": name,
            "first_name": first_name,
            "phone_number": phone_number,
            "qr_code": None,
        }
        pupils_store.put(
            name,
            **pupil_data,
        )
        print(f"You successfully created a new pupil! {pupil_data}")
        return True
    except JSONDecodeError as e:
        print(f"Create new pupil error: {e}")
        return False


def add_qr_code_data_to_pupil_by_name(pupil_name: str, qr_code_data: str) -> bool:
    try:
        pupil_data = get_pupil_data_by_name(pupil_name)
        if pupil_data:
            pupil_data["qr_code"] = qr_code_data
            pupils_store.put(pupil_name, **pupil_data)
            print(f"You successfully assign QR data to pupil: {pupil_name}, {qr_code_data}")
            return True
        return False
    except Exception as e:
        print(f"Add qr code to pupil with name {pupil_name} error: {e}")
        return False


def get_pupil_data_by_name(pupil_name: str) -> Optional[dict]:
    try:
        pupil_data = None
        find_result: Generator = pupils_store.find(name=pupil_name)
        for item in find_result:
            # Hint: item is a tuple of key and value
            if item:
                pupil_data = item[1]
                break
        return pupil_data
    except Exception as e:
        import traceback
        print(f"Get pupil data error: {e}, {traceback.format_exc()}")


def get_all_pupils() -> Optional[dict]:
    try:
        all_pupils = dict(pupils_store)
        return all_pupils
    except Exception as e:
        print(f"Create new pupil error: {e}")


# Active days crud
def activate_day(date: datetime.datetime) -> bool:
    try:
        str_date = str(date.date())
        active_days_storage.put(str_date, date=str_date, datetime=str(date))
        print(f"You're successfully activate {str_date} day!")
        return True
    except Exception as e:
        print(f"Error activate day: {e}")
        return False


def deactivate_day(date: datetime.date) -> bool:
    try:
        active_days_storage.delete(str(date))
        print(f"You're successfully deactivate {date} day!")
        return True
    except Exception as e:
        print(f"Error activate day: {e}")
        return False


def get_day_info_by_date(date: datetime.date) -> Optional[dict]:
    try:
        day_info = None
        day_info_result: Generator = active_days_storage.find(date=str(date))
        for item in day_info_result:
            # Hint: item is a tuple of key and value
            if item:
                day_info = item[1]
                break
        return day_info
    except Exception as e:
        print(f"Get day info error: {e}")


def get_activated_days() -> Optional[dict]:
    try:
        all_days = dict(active_days_storage)
        return all_days
    except Exception as e:
        print(f"Get activated days error: {e}")


# QR codes
def add_qr_code_record(qr_code: str) -> bool:
    try:
        current_data = datetime.datetime.now()
        unique_together_key = f"{current_data.date()}/{qr_code}"
        qr_codes_store.put(
            unique_together_key, unique_together=unique_together_key, datetime=str(current_data), qr_code=qr_code
        )  # -datetime.timedelta(hours=6)
        print(f"You're successfully added QR code {qr_code} to {current_data} datetime!")
        return True
    except Exception as e:
        print(f"Add QR code {qr_code} error: {e}")
        return False


def get_qr_code_record(date: datetime.date, qr_code: str) -> Optional[dict]:
    if not date or not qr_code:
        return None
    try:
        qr_code_record = None
        unique_together_key = f"{date}/{qr_code}"
        day_info_result: Generator = qr_codes_store.find(unique_together=unique_together_key)
        for item in day_info_result:
            # Hint: item is a tuple of key and value
            if item:
                qr_code_record = item[1]
                break
        return qr_code_record
    except Exception as e:
        print(f"Get qr code record error: {e}")


def get_qr_code_records() -> Optional[dict]:
    try:
        all_qr_code_records = dict(active_days_storage)
        return all_qr_code_records
    except Exception as e:
        print(f"Get QR codes records error: {e}")
