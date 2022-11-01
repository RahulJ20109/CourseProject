import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd

# function to verify insurance_company_record id


def verify_insurance_company_record_id(insurance_company_record_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM insurance_company_record_record;
            """
        )
    for id in c.fetchall():
        if id[0] == insurance_company_record_id:
            verify = True
            break
    conn.close()
    return verify

# function to generate unique insurance_company_record id using current date and time


def generate_insurance_company_record_id(reg_date, reg_time):
    id_1 = ''.join(reg_time.split(':')[::-1])
    id_2 = ''.join(reg_date.split('-')[::-1])[2:]
    id = f'I-{id_1}-{id_2}'
    return id


# function to show the details of insurance_company_record(s) given in a list (provided as a parameter)


def show_insurance_company_record_details(list_of_insurance_company_records):
    insurance_company_record_titles = ['insurance_company_record ID', 'Name', 'Contact number', 'Alternate contact number',
                                       'Address', 'City', 'State', 'PIN code', 'Email ID', 'Description']
    insurance_company_record_details = []
    conn, c = db.connection()
    for insurance_company_record_id in list_of_insurance_company_records:
        with conn:
            c.execute(
                """
                SELECT *
                FROM insurance_company_record_record
                WHERE id = :id;
                """,
                {'id': insurance_company_record_id}
            )
        insurance_company_record_details.append(c.fetchone())
    conn.close()
    insurance_company_record_details = pd.DataFrame(
        insurance_company_record_details, columns=insurance_company_record_titles)
    st.table(insurance_company_record_details)
    if len(list_of_insurance_company_records) == 0:
        st.warning('No data to show')
    elif len(list_of_insurance_company_records) == 1:
        insurance_company_record_details = [
            x for x in list_of_insurance_company_records[0]]
        series = pd.Series(data=insurance_company_record_details,
                           index=insurance_company_record_titles)
        st.write(series)
    else:
        insurance_company_record_details = []
        for insurance_company_record in list_of_insurance_company_records:
            insurance_company_record_details.append(
                [x for x in insurance_company_record])
        df = pd.DataFrame(data=insurance_company_record_details,
                          columns=insurance_company_record_titles)
        st.write(df)

# class containing all the fields and methods required to work with the insurance_company_records' table in the database


class InsuranceCompany:
    def __init__(self):
        self.name = str()
        self.id = str()
        self.username = str()
        self.password = str()
        self.verification_document = str()
        self.contact_number_1 = str()
        self.contact_number_2 = str()
        self.date_of_registration = str()
        self.time_of_registration = str()
        self.email_id = str()
        self.address = str()
        self.city = str()
        self.state = str()
        self.pin_code = str()
        self.description = str()

    # method to add a new insurance_company_record record to the database
    def add_insurance_company_record(self):
        st.write('Enter insurance_company_record details:')
        self.name = st.text_input('Full name')
        st.write('Enter Password')
        self.password = st.text_input('Password', type='password')
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
        self.description = st.text_input('Description')
        self.date_of_registration = datetime.now().strftime('%d-%m-%Y')
        self.time_of_registration = datetime.now().strftime('%H:%M:%S')
        self.id = generate_insurance_company_record_id(self.date_of_registration,
                                                       self.time_of_registration)
        self.verification_document = st.text_input('Verification document')
        save = st.button('Save')

        # executing SQLite statements to save the new insurance_company_record record to the database
        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO insurance_company_record_record
                    (
                        id,username, password, name,verification_document
                        contact_number_1, contact_number_2,address,city, state, pin_code,email_id,
                        date_of_registration, time_of_registration, description
                    )
                    VALUES (
                        :id,:username,:password :name,:verification_document
                        :phone_1, :phone_2,
                        :address, :city, :state, :pin,:email_id,
                        :reg_date, :reg_time, :description
                    );
                    """,
                    {
                        'id': self.id, 'username': self.username, 'password': self.password,
                        'name': self.name, 'verification_document': self.verification_document,
                        'phone_1': self.contact_number_1,
                        'phone_2': self.contact_number_2,
                        'address': self.address,
                        'city': self.city, 'state': self.state,
                        'pin': self.pin_code, 'email_id': self.email_id,
                        'reg_date': self.date_of_registration,
                        'reg_time': self.time_of_registration,
                        'description': self.description
                    }
                )
            st.success('Insurance Company Record details saved successfully.')
            st.write('Your insurance_company_record ID is: ', self.id)
            conn.close()

    # method to verify insurance_company_record details by admmin
    # def verify_insurance_company_record(self):

    # method to update an existing insurance_company_record record in the database

    def update_insurance_company_record(self):
        id = st.text_input('Enter ID of the Insurance Company to be updated')
        if id == '':
            st.empty()
        elif not verify_insurance_company_record_id(id):
            st.error('Invalid insurance_company_record ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the insurance_company_record before updating
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM insurance_company_record_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write(
                    'Here are the current details of the insurance_company_record:')
                show_insurance_company_record_details(c.fetchall())

            st.write('Enter new details of the insurance_company_record:')
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

            # executing SQLite statements to update this insurance_company_record's record in the database
            if update:

                with conn:
                    c.execute(
                        """
                        UPDATE insurance_company_record_record
                        SET contact_number_1 = :phone_1,
                        contact_number_2 = :phone_2,address = :address, city = :city,
                        state = :state, pin_code = :pin,email_id = :email_id
                        WHERE id = :id;
                        """,
                        {
                            'id': id,
                            'phone_1': self.contact_number_1,
                            'phone_2': self.contact_number_2,
                            'address': self.address, 'city': self.city,
                            'state': self.state, 'pin': self.pin_code,
                            'email_id': self.email_id
                        }
                    )
                st.success(
                    'insurance_company_record details updated successfully.')
                conn.close()

    # method to delete an existing insurance_company_record record from the database
    def delete_insurance_company_record(self):
        id = st.text_input(
            'Enter insurance_company_record ID of the insurance_company_record to be deleted')
        if id == '':
            st.empty()
        elif not verify_insurance_company_record_id(id):
            st.error('Invalid insurance_company_record ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the insurance_company_record before deletion
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM insurance_company_record_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write(
                    'Here are the details of the insurance_company_record to be deleted:')
                show_insurance_company_record_details(c.fetchall())

                confirm = st.checkbox('Check this box to confirm deletion')
                if confirm:
                    delete = st.button('Delete')

                    # executing SQLite statements to delete this insurance_company_record's record from the database
                    if delete:
                        c.execute(
                            """
                            DELETE FROM insurance_company_record_record
                            WHERE id = :id;
                            """,
                            {'id': id}
                        )
                        st.success(
                            'insurance_company_record details deleted successfully.')
            conn.close()

    # method to show the complete insurance_company_record record
    def show_all_insurance_company_records(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM insurance_company_record_record;
                """
            )
            show_insurance_company_record_details(c.fetchall())
        conn.close()

    # method to search and show a particular insurance_company_record's details in the database using insurance_company_record id
    def search_insurance_company_record(self):
        id = st.text_input(
            'Enter insurance_company_record ID of the insurance_company_record to be searched')
        if id == '':
            st.empty()
        elif not verify_insurance_company_record_id(id):
            st.error('Invalid insurance_company_record ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM insurance_company_record_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write(
                    'Here are the details of the insurance_company_record you searched for:')
                show_insurance_company_record_details(c.fetchall())
            conn.close()
