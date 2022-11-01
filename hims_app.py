import sqlite3 as sql
import streamlit as st
import database as db
from healthCareProfessional import HealthCareProfessional
from insuranceCompany import InsuranceCompany
from hospital import Hospital
from patient import Patient
# from department import Department
# from doctor import Doctor
# from prescription import Prescription
# from medical_test import Medical_Test
from pharmacy import Pharmacy
import config


# function to verify edit mode password


def verify_edit_mode_password():
    edit_mode_password = st.sidebar.text_input(
        'Enter edit mode password', type='password')
    if edit_mode_password == config.edit_mode_password:
        st.sidebar.success('Verified')
        return True
    elif edit_mode_password == '':
        st.empty()
    else:
        st.sidebar.error('Invalid edit mode password')
        return False

# function to verify doctor/medical lab scientist access code


def verify_dr_mls_access_code():
    dr_mls_access_code = st.sidebar.text_input(
        'Enter doctor/medical lab scientist access code', type='password')
    if dr_mls_access_code == config.dr_mls_access_code:
        st.sidebar.success('Verified')
        return True
    elif dr_mls_access_code == '':
        st.empty()
    else:
        st.sidebar.error('Invalid access code')
        return False

# function to perform various operations of the patient module (according to user's selection)


def patients():
    st.header('PATIENTS')
    option_list = ['', 'Add patient', 'Update patient',
                   'Delete patient', 'Show complete patient record', 'Search patient']
    option = st.sidebar.selectbox('Select function', option_list)
    p = Patient()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]):
        if option == option_list[1]:
            st.subheader('ADD PATIENT')
            p.add_patient()
        elif option == option_list[2]:
            st.subheader('UPDATE PATIENT')
            p.update_patient()
        elif option == option_list[3]:
            st.subheader('DELETE PATIENT')
            try:
                p.delete_patient()
            # handles foreign key constraint failure issue (due to integrity error)
            except sql.IntegrityError:
                st.error(
                    'This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE PATIENT RECORD')
        p.show_all_patients()
    elif option == option_list[5]:
        st.subheader('SEARCH PATIENT')
        p.search_patient()


# function to perform various operations of the doctor module (according to user's selection)


def healthCareProfessionals():
    st.header('HEALTH CARE PROFESSIONAL')
    option_list = ['', 'Add Health Care Professional', 'Update Health Care Professional',
                   'Delete Health Care Professional', 'Show complete Health Care Professional record', 'Search Health Care Professional']
    option = st.sidebar.selectbox('Select function', option_list)
    hcr = HealthCareProfessional()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]):
        if option == option_list[1]:
            st.subheader('ADD HEALTH CARE PROFESSIONAL')
            hcr.add_healthCareProfessional()
        elif option == option_list[2]:
            st.subheader('UPDATE HEALTH CARE PROFESSIONAL')
            hcr.update()
        elif option == option_list[3]:
            st.subheader('DELETE HEALTH CARE PROFESSIONAL')
            try:
                hcr.delete_professional()
            # handles foreign key constraint failure issue (due to integrity error)
            except sql.IntegrityError:
                st.error(
                    'This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE HEALTH CARE PROFESSIONAL RECORD')
        hcr.show_all_professionals()
    elif option == option_list[5]:
        st.subheader('SEARCH HEALTH CARE PROFESSIONAL')
        hcr.search_professional()


def hospitals():
    st.header('HOSPITALS')
    option_list = ['', 'Add Hospital', 'Update Hospital',
                   'Delete Hospital', 'Show complete Hospital record', 'Search Hospital']
    option = st.sidebar.selectbox('Select function', option_list)

    hos = Hospital()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]):
        if option == option_list[1]:
            st.subheader('ADD HOSPITAL')
            hos.add_hospital()
        elif option == option_list[2]:
            st.subheader('UPDATE HOSPITAL')
            hos.update_hospital()
        elif option == option_list[3]:
            st.subheader('DELETE HOSPITAL')
            try:
                hos.delete_hospital()
            # handles foreign key constraint failure issue (due to integrity error)
            except sql.IntegrityError:
                st.error(
                    'This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE HOSPITAL RECORD')
        hos.show_all_hospitals()
    elif option == option_list[5]:
        st.subheader('SEARCH HOSPITAL')
        hos.search_hospital()
# function to perform various operations of the prescription module (according to user's selection)


def pharmacys():
    st.header('PHARMACYS')
    option_list = ['', 'Add Pharmacy', 'Update Pharmacy',
                   'Delete Pharmacy', 'Show complete Pharmacy record', 'Search Pharmacy']
    option = st.sidebar.selectbox('Select function', option_list)

    hos = Pharmacy()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]):
        if option == option_list[1]:
            st.subheader('ADD Pharmacy')
            hos.add_pharmacy()
        elif option == option_list[2]:
            st.subheader('UPDATE Pharmacy')
            hos.update_pharmacy()
        elif option == option_list[3]:
            st.subheader('DELETE Pharmacy')
            try:
                hos.delete_pharmacy()
            # handles foreign key constraint failure issue (due to integrity error)
            except sql.IntegrityError:
                st.error(
                    'This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE Pharmacy RECORD')
        hos.show_all_pharmacys()
    elif option == option_list[5]:
        st.subheader('SEARCH Pharmacy')
        hos.search_pharmacy()


def insuranceCompanys():
    st.header('INSURANCE COMPANY')
    option_list = ['', 'Add Insurance Company', 'Update Insurance Company',
                   'Delete Insurance Company', 'Show complete Insurance Company record', 'Search Insurance Company']
    option = st.sidebar.selectbox('Select function', option_list)

    hos = InsuranceCompany()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]):
        if option == option_list[1]:
            st.subheader('ADD Insurance Company')
            hos.add_insurance_company_record()
        elif option == option_list[2]:
            st.subheader('UPDATE Insurance Company')
            hos.update_insurance_company_record()
        elif option == option_list[3]:
            st.subheader('DELETE Insurance Company')
            try:
                hos.delete_insurance_company_record()
            # handles foreign key constraint failure issue (due to integrity error)
            except sql.IntegrityError:
                st.error(
                    'This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE Insurance Company RECORD')
        hos.search_insurance_company_record()
    elif option == option_list[5]:
        st.subheader('SEARCH Insurance Company')
        hos.search_insurance_company_record()


# function to implement and initialise login menu


def login(str):
    st.header('LOGIN')
    st.subheader('Please enter your credentials')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if verify_login(str, username, password):
            return True
            # Specific function calling for each user type
        else:
            st.error('Invalid username or password')

# function to implement and initialise registration menu


def register(str):
    st.header('REGISTER')
    st.subheader('Please enter your details')
    id = st.text_input('ID')
    if st.button('Register'):
        # if password == confirm_password:
        if verify_registration(str, id):
            if (str == 'patient_record'):
                p = Patient()
                p.add_patient()
            elif (str == 'healthCareProfessional_record'):
                healthCareProfessionals().add_healthCareProfessional()
            elif (str == 'hospital_record'):
                hospitals().add_hospital()
            elif (str == 'pharmacy_record'):
                pharmacys().add_pharmacy()
            elif (str == 'insurance_company_record'):
                insuranceCompanys().add_insuranceCompany()

        else:
            st.error('Username already exists')
        # else:
        #     st.error('Passwords do not match')

# function to implement verify login credentials


def verify_login(type, username, password):
    # establish connection to the database
    conn, c = db.connection()
    with conn:
        c.execute('SELECT * FROM ' + type + ' WHERE username = :username AND password = :password',
                  {'username': username, 'password': password})
        data = c.fetchone()
    conn.close()
    if data:
        return True
    else:
        return False

# function to implement verify registration credentials


def verify_registration(type, id):
    st.write(type)
    conn, c = db.connection()
    with conn:
        c.execute('SELECT * FROM '+type+' WHERE id = :id',
                  {'id': id})
        result = c.fetchone()
    conn.close()
    if not result:
        return True
    # return the result
    return False


# Starting point of the program
st.title('HEALTHCARE INFORMATION MANAGEMENT SYSTEM')
option1 = st.sidebar.selectbox('Select option', ['', 'User', 'Organization'])
db.db_init()
if option1 == 'User':
    option2 = st.sidebar.selectbox(
        'Select option', ['', 'Patient', 'HealthCare Professional'])
    if option2 == 'Patient':
        option3 = st.sidebar.selectbox(
            'Select option', ['', 'Login', 'Register'])
        str = "patient_record"
        if option3 == 'Login':
            if login(str):
                patients()
        elif option3 == 'Register':
            register(str)
    elif option2 == 'HealthCare Professional':
        str = "healthCareProfessional_record"
        option3 = st.sidebar.selectbox(
            'Select option', ['', 'Login', 'Register'])
        if option3 == 'Login':
            if login(str):
                healthCareProfessionals()
        elif option3 == 'Register':
            register(str)
elif option1 == 'Organization':
    option2 = st.sidebar.selectbox(
        'Select option', ['', 'Hospital', 'Pharmacy', 'Insurance Firm'])
    if option2 == 'Hospital':
        option3 = st.sidebar.selectbox(
            'Select option', ['', 'Login', 'Register'])
        str = "hospital_record"
        if option3 == 'Login':
            if login(str):
                hospitals()
        elif option3 == 'Register':
            register(str)
    elif option2 == 'Pharmacy':
        str = "pharmacy_record"
        option3 = st.sidebar.selectbox(
            'Select option', ['', 'Login', 'Register'])
        if option3 == 'Login':
            if login(str):
                pharmacys()
        elif option3 == 'Register':
            register(str)
    elif option2 == 'Insurance Firm':
        str = "insurance_company_record"
        option3 = st.sidebar.selectbox(
            'Select option', ['', 'Login', 'Register'])
        if option3 == 'Login':
            if login(str):
                insuranceCompanys()
        elif option3 == 'Register':
            register(str)
