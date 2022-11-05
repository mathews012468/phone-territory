import os
import datetime
from enum import Enum

DATABASE_FOLDER = "numbers"

class PhoneInfo:
    def __init__(self, phone_number, name=None, address=None, call_outcome=None):
        self.phone_number = phone_number
        self.name = name
        self.address = address
        self.call_outcome = call_outcome


class FileType(Enum):
    NAMES = "names"
    ADDRESSES = "addresses"
    CALL_OUTCOMES = "call-outcomes"


def prepare_phone_folder(phone_path):
    """
    Given a folder, creates files called names, addresses, and call-outcomes
    Assumes folder already exists

    phone_path: path to the phone number's folder
    """
    #   add files to that folder called names, addresses, and call-outcomes
    names_file = os.path.join(phone_path, FileType.NAMES.value)
    f = open(names_file, "w"); f.close()

    addresses_file = os.path.join(phone_path, FileType.ADDRESSES.value)
    f = open(addresses_file, "w"); f.close()

    call_outcomes_file = os.path.join(phone_path, FileType.CALL_OUTCOMES.value)
    f = open(call_outcomes_file, "w"); f.close()

def update_name(phone_number, name, date):
    """
    Update name associated with phone number.
    Only adds name if name is different from most recent name

    Assumes phone number folder exists and has a file called names

    return True if new name was added
    """
    #do nothing if the name we're adding is already the most recent name
    names_path = os.path.join(DATABASE_FOLDER, phone_number, FileType.NAMES.value)
    with open(names_path) as f:
        #if there are no current names for the phone number,
        #calling next will cause a StopIteration which stops
        # the rest of the program from running. If there is 
        # a StopIteration, that means that the new name we're 
        # adding is definitely not a repeat, so we should add it.
        try:
            most_recent_name = next(f).split(".")[0]
            if name.lower() == most_recent_name.lower():
                return False
        except StopIteration:
            pass

    update_file(
        phone_number=phone_number,
        file_type=FileType.NAMES,
        record=name,
        date=date
    )
    return True

def update_address(phone_number, address, date):
    """
    Update address associated with phone number.
    Only adds address if address is different from most recent address

    Assumes phone number folder exists and has a file called addresses

    return True if new address was added
    """
    #do nothing if the name we're adding is already the most recent name
    addresses_path = os.path.join(DATABASE_FOLDER, phone_number, FileType.ADDRESSES.value)
    with open(addresses_path) as f:
        #if there are no current addresses, we get a StopIteration, 
        # which means we should add the current address.
        try:
            most_recent_address = next(f).split(".")[0]
            if address.lower() == most_recent_address.lower():
                return False
        except StopIteration:
            pass
    
    update_file(
        phone_number=phone_number,
        file_type=FileType.ADDRESSES,
        record=address,
        date=date
    )
    return True

def update_call_outcome(phone_number, call_outcome, date):
    """
    Update call outcome associated with phone number.  
    Assumes phone number folder exists and has a file called call-outcomes  
    return True if new call outcome was added (for now this is always True)
    """    
    update_file(
        phone_number=phone_number,
        file_type=FileType.CALL_OUTCOMES,
        record=call_outcome,
        date=date
    )
    return True

def update_file(phone_number, file_type, record, date):
    """
    Update file with new record

    phone_number: 10 digit string
    file_type: FileType, one of names, addresses, call_outcomes
    record: one of a name, address, or call outcome. string
    date: date of update, in the format MM-DD-YYYY
    """
    records_file = os.path.join(DATABASE_FOLDER, phone_number, file_type.value)
    with open(records_file, "r+") as f:
        records = [line.strip() for line in f.readlines()]
        #most recent records appear at the beginning of the file
        records.insert(0, f"{record}.{date}")

        del records[10:] #no more than ten names
        f.seek(0); f.truncate() #clear all contents
        f.write("\n".join(records)) #write new contents


def add_and_update_numbers(phone_info):
    """
    phone_info: PhoneInfo
    """
    #THINGS I WANT TO BE TRUE
    #1. At least one of name, address, and call outcome has a value (is not None)
    #2. Phone number should be a ten digit string
    #3. Name should have no periods
    #4. Address should have no periods

    phone_path = os.path.join(DATABASE_FOLDER, phone_info.phone_number)
    #if number is not already in database:
    if not os.path.exists(phone_path):
        #add it to the database, which consists of:
        #   creating a folder named the phone number
        os.mkdir(phone_path)
        #   adding files to that folder called names, addresses, and call-outcomes
        prepare_phone_folder(phone_path)

    #update phone info
    today = datetime.date.today().strftime("%m-%d-%Y")
    if phone_info.name is not None:
        #insert new name and date in first line
        #only if name is different from most recent name
        update_name(
            phone_number=phone_info.phone_number, 
            name=phone_info.name, 
            date=today
        )
        
    if phone_info.address is not None:
        #insert new address and date in first line
        #only if address is different from most recent name
        update_address(
            phone_number=phone_info.phone_number, 
            address=phone_info.address, 
            date=today
        )
    
    if phone_info.call_outcome is not None:
        #insert new call outcome and date in first line
        update_call_outcome(
            phone_number=phone_info.phone_number, 
            call_outcome=phone_info.call_outcome, 
            date=today
        )
