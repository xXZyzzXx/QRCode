from uuid import uuid4
from typing import Optional, Generator
from json.decoder import JSONDecodeError

from kivy.storage.jsonstore import JsonStore

from app.utils import create_database_folder


create_database_folder()
pupils_store = JsonStore('db/pupils_db.json')


def create_new_pupil(name: str, first_name: str, phone_number: str) -> bool:
    try:
        pupil_id = str(uuid4())
        pupil_data = {
            "pupil_id": pupil_id,
            "name": name,
            "first_name": first_name,
            "phone_number": phone_number,
        }
        pupils_store.put(
            name,
            **pupil_data,
        )
        return True
    except JSONDecodeError as e:
        print(f"Create new pupil error: {e}")
        return False


def get_pupil_data_by_name(pupil_name: str) -> Optional[dict]:
    try:
        pupil_data = None
        find_result: Generator = pupils_store.find(name=pupil_name)
        for item in find_result:
            # item is a tuple of key and value
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
