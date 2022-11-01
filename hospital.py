import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd

# function to verify hospital id


def verify_hospital_id(hospital_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM hospital_record;
            """
        )
    for id in c.fetchall():
        if id[0] == hospital_id:
            verify = True
            break
    conn.close()
    return verify

# function to generate unique hospital id using current date and time


def generate_hospital_id(reg_date, reg_time):
    id_1 = ''.join(reg_time.split(':')[::-1])
    id_2 = ''.join(reg_date.split('-')[::-1])[2:]
    id = f'Hos-{id_1}-{id_2}'
    return id


# function to show the details of hospital(s) given in a list (provided as a parameter)


def show_hospital_details(list_of_hospitals):
    hospital_titles = ['hospital ID', 'Name', 'Contact number', 'Alternate contact number',
                       'Address', 'City', 'State', 'PIN code', 'Email ID', 'Description']
    hospital_details = []
    conn, c = db.connection()
    for hospital_id in list_of_hospitals:
        with conn:
            c.execute(
                """
                SELECT *
                FROM hospital_record
                WHERE id = :id;
                """,
                {'id': hospital_id}
            )
        hospital_details.append(c.fetchone())
    conn.close()
    hospital_details = pd.DataFrame(hospital_details, columns=hospital_titles)
    st.table(hospital_details)
    if len(list_of_hospitals) == 0:
        st.warning('No data to show')
    elif len(list_of_hospitals) == 1:
        hospital_details = [x for x in list_of_hospitals[0]]
        series = pd.Series(data=hospital_details, index=hospital_titles)
        st.write(series)
    else:
        hospital_details = []
        for hospital in list_of_hospitals:
            hospital_details.append([x for x in hospital])
        df = pd.DataFrame(data=hospital_details, columns=hospital_titles)
        st.write(df)

# class containing all the fields and methods required to work with the hospitals' table in the database


class Hospital:
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

    # method to add a new hospital record to the database
    def add_hospital(self):
        st.write('Enter hospital details:')
        self.name = st.text_input('Full name')
        st.write('Enter password:')
        self.password = st.text_input('', type='password')
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
        self.id = generate_hospital_id(self.date_of_registration,
                                       self.time_of_registration)
        self.verification_document = st.text_input('Verification document')
        save = st.button('Save')

        # executing SQLite statements to save the new hospital record to the database
        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO hospital_record
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
            st.success('hospital details saved successfully.')
            st.write('Your hospital ID is: ', self.id)
            conn.close()

    # method to verify hospital details by admmin
    # def verify_hospital(self):

    # method to update an existing hospital record in the database

    def update_hospital(self):
        id = st.text_input('Enter hospital ID of the hospital to be updated')
        if id == '':
            st.empty()
        elif not verify_hospital_id(id):
            st.error('Invalid hospital ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the hospital before updating
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM hospital_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Here are the current details of the hospital:')
                show_hospital_details(c.fetchall())

            st.write('Enter new details of the hospital:')
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

            # executing SQLite statements to update this hospital's record in the database
            if update:

                with conn:
                    c.execute(
                        """
                        UPDATE hospital_record
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
                st.success('hospital details updated successfully.')
                conn.close()

    # method to delete an existing hospital record from the database
    def delete_hospital(self):
        id = st.text_input('Enter hospital ID of the hospital to be deleted')
        if id == '':
            st.empty()
        elif not verify_hospital_id(id):
            st.error('Invalid hospital ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the hospital before deletion
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM hospital_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Here are the details of the hospital to be deleted:')
                show_hospital_details(c.fetchall())

                confirm = st.checkbox('Check this box to confirm deletion')
                if confirm:
                    delete = st.button('Delete')

                    # executing SQLite statements to delete this hospital's record from the database
                    if delete:
                        c.execute(
                            """
                            DELETE FROM hospital_record
                            WHERE id = :id;
                            """,
                            {'id': id}
                        )
                        st.success('hospital details deleted successfully.')
            conn.close()

    # method to show the complete hospital record
    def show_all_hospitals(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM hospital_record;
                """
            )
            show_hospital_details(c.fetchall())
        conn.close()

    # method to search and show a particular hospital's details in the database using hospital id
    def search_hospital(self):
        id = st.text_input('Enter hospital ID of the hospital to be searched')
        if id == '':
            st.empty()
        elif not verify_hospital_id(id):
            st.error('Invalid hospital ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM hospital_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Here are the details of the hospital you searched for:')
                show_hospital_details(c.fetchall())
            conn.close()
