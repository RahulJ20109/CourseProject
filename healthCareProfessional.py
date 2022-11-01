import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd

# function to verify patient id


def verify_id(id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM healthCareProfessional_record;
            """
        )
    for id in c.fetchall():
        if id[0] == id:
            verify = True
            break
    conn.close()
    return verify

# function to generate unique patient id using current date and time


def generate_id(reg_date, reg_time):
    id_1 = ''.join(reg_time.split(':')[::-1])
    id_2 = ''.join(reg_date.split('-')[::-1])[2:]
    id = f'H-{id_1}-{id_2}'
    return id


def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - \
        ((dob.month, dob.day) > (today.month, today.day))
    return age
# function to show the details of patient(s) given in a list (provided as a parameter)


def show_details(list_of_professionals):
    titles = ['ID', 'Name', 'Age', 'Gender', 'Date of birth (DD-MM-YYYY)',
              'Contact number', 'Alternate contact number']
    if len(list_of_professionals) == 0:
        st.warning('No data to show')
    elif len(list_of_professionals) == 1:
        details = [x for x in list_of_professionals[0]]
        series = pd.Series(data=details, index=titles)
        st.write(series)
    else:
        details = []
        for professional in list_of_professionals:
            details.append([x for x in professional])
        df = pd.DataFrame(data=details, columns=titles)
        st.write(df)

# class containing all the fields and methods required to work with the patients' table in the database


class HealthCareProfessional:

    def __init__(self):
        """
        id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                contact_number_1 TEXT NOT NULL,
                contact_number_2 TEXT,
                verification_document TEXT NOT NULL UNIQUE,
                email_id TEXT NOT NULL UNIQUE,
                qualification TEXT NOT NULL,
                specialisation TEXT NOT NULL,
                years_of_experience INTEGER NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                pin_code TEXT NOT NULL,
        """
        self.name = str()
        self.id = str()
        self.username = str()
        self.password = str()
        self.verification_document = str()
        self.gender = str()
        self.age = int()
        self.contact_number_1 = str()
        self.contact_number_2 = str()
        self.date_of_birth = str()
        self.blood_group = str()
        self.email_id = str()
        self.address = str()
        self.city = str()
        self.state = str()
        self.pin_code = str()
        self.qualification = str()
        self.specialisation = str()
        self.years_of_experience = int()
        self.address = str()
        self.city = str()
        self.state = str()
        self.time_of_registration = str()
        self.date_of_registration = str()

    # method to add a new patient record to the database

    def add_healthCareProfessional(self):
        st.write('Enter details:')
        self.name = st.text_input('Full name')
        st.write('Enter Password')
        self.password = st.text_input('Password', type='password')
        gender = st.radio('Gender', ['Female', 'Male', 'Other'])
        if gender == 'Other':
            gender = st.text_input('Please mention')
        self.gender = gender
        dob = st.date_input('Date of birth (YYYY/MM/DD)')
        st.info(
            'If the required date is not in the calendar, please type it in the box above.')
        # converts date of birth to the desired string format
        self.date_of_birth = dob.strftime('%d-%m-%Y')
        self.age = calculate_age(dob)
        self.blood_group = st.text_input('Blood group')
        self.contact_number_1 = st.text_input('Contact number')
        contact_number_2 = st.text_input('Alternate contact number (optional)')
        self.contact_number_2 = (
            lambda phone: None if phone == '' else phone)(contact_number_2)
        self.address = st.text_area('Address')
        self.city = st.text_input('City')
        self.state = st.text_input('State')
        self.pin_code = st.text_input('PIN code')
        email_id = st.text_input('Email ID (optional)')
        self.email_id = (lambda email: None if email ==
                         '' else email)(email_id)
        self.date_of_registration = datetime.now().strftime('%d-%m-%Y')
        self.time_of_registration = datetime.now().strftime('%H:%M:%S')
        self.id = generate_id(self.date_of_registration,
                              self.time_of_registration)
        self.verification_document = st.text_input('Verification document')
        save = st.button('Save')

        # executing SQLite statements to save the new patient record to the database
        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO healthCareProfessional_record
                    (
                        id,username, password, name, age, gender, date_of_birth, blood_group,verification_document
                        contact_number_1, contact_number_2, address,city, state, pin_code, email_id,
                        date_of_registration, time_of_registration
                    )
                    VALUES (
                        :id,:username,:password :name, :age, :gender, :dob, :blood_group,:verification_document
                        :phone_1, :phone_2, 
                        :address, :city, :state, :pin, :email_id,
                        :reg_date, :reg_time
                    );
                    """,
                    {
                        'id': self.id, 'username': self.username, 'password': self.password,
                        'name': self.name, 'age': self.age,
                        'gender': self.gender, 'dob': self.date_of_birth,
                        'blood_group': self.blood_group,
                        'verification_document': self.verification_document,
                        'phone_1': self.contact_number_1,
                        'phone_2': self.contact_number_2,
                        'address': self.address,
                        'city': self.city, 'state': self.state,
                        'pin': self.pin_code,
                        'email_id': self.email_id,
                        'reg_date': self.date_of_registration,
                        'reg_time': self.time_of_registration
                    }
                )
            st.success('Patient details saved successfully.')
            st.write('Your Patient ID is: ', self.id)
            conn.close()

    # method to verify patient details by admmin
    # def verify_patient(self):

    # method to update an existing patient record in the database

    def update(self):
        id = st.text_input(
            'Enter ID of the Health Care Professional to be updated')
        if id == '':
            st.empty()
        elif not verify_id(id):
            st.error('Invalid Patient ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the patient before updating
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM healthCareProfessional_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Here are the current details of the professional:')
                show_details(c.fetchall())

            st.write('Enter new details:')
            self.contact_number_1 = st.text_input('Contact number')
            contact_number_2 = st.text_input(
                'Alternate contact number (optional)')
            self.contact_number_2 = (
                lambda phone: None if phone == '' else phone)(contact_number_2)
            self.address = st.text_area('Address')
            self.city = st.text_input('City')
            self.state = st.text_input('State')
            self.pin_code = st.text_input('PIN code')
            email_id = st.text_input('Email ID (optional)')
            self.email_id = (lambda email: None if email ==
                             '' else email)(email_id)
            update = st.button('Update')

            # executing SQLite statements to update this patient's record in the database
            if update:
                with conn:
                    c.execute(
                        """
                        SELECT date_of_birth
                        FROM healthCareProfessional_record
                        WHERE id = :id;
                        """,
                        {'id': id}
                    )

                    # converts date of birth to the required format for age calculation
                    dob = [int(d) for d in c.fetchone()[0].split('-')[::-1]]
                    dob = date(dob[0], dob[1], dob[2])
                    self.age = calculate_age(dob)

                with conn:
                    c.execute(
                        """
                        UPDATE healthCareProfessional_record
                        SET age = :age, contact_number_1 = :phone_1,
                        contact_number_2 = :phone_2, address = :address, city = :city,
                        state = :state, pin_code = :pin,email_id = :email_id
                        WHERE id = :id;
                        """,
                        {
                            'id': id, 'age': self.age,
                            'phone_1': self.contact_number_1,
                            'phone_2': self.contact_number_2,
                            'address': self.address, 'city': self.city,
                            'state': self.state, 'pin': self.pin_code,
                            'email_id': self.email_id
                        }
                    )
                st.success('Details updated successfully.')
                conn.close()

    # method to delete an existing patient record from the database
    def delete_professional(self):
        id = st.text_input('Enter ID of the professional to be deleted')
        if id == '':
            st.empty()
        elif not verify_id(id):
            st.error('Invalid ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the patient before deletion
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM healthCareProfessional_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Here are the details of the professional to be deleted:')
                show_details(c.fetchall())

                confirm = st.checkbox('Check this box to confirm deletion')
                if confirm:
                    delete = st.button('Delete')

                    # executing SQLite statements to delete this patient's record from the database
                    if delete:
                        c.execute(
                            """
                            DELETE FROM healthCareProfessional_record
                            WHERE id = :id;
                            """,
                            {'id': id}
                        )
                        st.success('Details deleted successfully.')
            conn.close()

    # method to show the complete patient record
    def show_all_professionals(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM healthCareProfessional_record;
                """
            )
            show_details(c.fetchall())
        conn.close()

    # method to search and show a particular patient's details in the database using patient id
    def search_professional(self):
        id = st.text_input('Enter ID of the professional to be searched')
        if id == '':
            st.empty()
        elif not verify_id(id):
            st.error('Invalid ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM healthCareProfessional_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write(
                    'Here are the details of the professional you searched for:')
                show_details(c.fetchall())
            conn.close()
