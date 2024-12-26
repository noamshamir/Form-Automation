from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import os
import math
from typing import List

# File paths
plaintiff_excel_data_path = '/Users/noamshamir/Documents/Mabel/Form Automation/in/SIJ_excel_test.xlsx'
defendant_excel_data_path = '/Users/noamshamir/Documents/Mabel/Form Automation/in/defendent_excel.xlsx'

def get_dicts(file_path):
    """Convert Excel file to list of dictionaries"""
    data = pd.read_excel(file_path, header=5)
    return data.to_dict(orient='records')

def get_form_fields(plaintiff_data, defendant_data, attorney_data):
    # TODO age and dob
    print(f"Plaintiff data: {plaintiff_data}")
    print(f"Defendant data: {defendant_data}")
    print(f"Attorney data: {attorney_data}")
    cjd109_fields = {
        'form1[0].BodyPage1[0].Subform6[0].TextField4[4]': plaintiff_data['first_name'],
        'form1[0].BodyPage1[0].Subform6[0].TextField4[5]': plaintiff_data['last_name'],
        'form1[0].BodyPage1[0].Subform6[0].TextField4[1]': defendant_data['first_name'],
        'form1[0].BodyPage1[0].Subform6[0].TextField4[2]': defendant_data['last_name'],
        'form1[0].BodyPage1[0].Subform6[0].TextField4[3]': defendant_data['middle_initial'],
        'form1[0].BodyPage1[0].Subform6[0].TextField4[6]': defendant_data['middle_initial'],
        
        'form1[0].BodyPage1[0].S1[0].t1[0]': plaintiff_data['address'],
        'form1[0].BodyPage1[0].S1[0].TextField4[1]': plaintiff_data['apartment_number'],
        'form1[0].BodyPage1[0].S1[0].t2[0]': plaintiff_data['city'],
        'form1[0].BodyPage1[0].S1[0].TextField4[0]': plaintiff_data['state'],
        'form1[0].BodyPage1[0].S1[0].TextField5[0]': plaintiff_data['zip_code'],
        
        'form1[0].BodyPage1[0].S2[0].TextField4[2]': plaintiff_data['first_name'],
        'form1[0].BodyPage1[0].S2[0].TextField4[1]': plaintiff_data['middle_initial'],
        'form1[0].BodyPage1[0].S2[0].TextField4[0]': plaintiff_data['last_name'],
        # 'form1[0].BodyPage1[0].S2[0].TextField5[1]': plaintiff_data['age'],
        # 'form1[0].BodyPage1[0].S2[0].TextField5[2]': plaintiff_data['date_of_birth'],
        'form1[0].BodyPage1[0].S2[0].TextField4[6]': plaintiff_data['address'],
        'form1[0].BodyPage1[0].S2[0].TextField4[5]': plaintiff_data['apartment_number'],
        'form1[0].BodyPage1[0].S2[0].TextField4[4]': plaintiff_data['city'],
        'form1[0].BodyPage1[0].S2[0].TextField4[3]': plaintiff_data['state'],
        'form1[0].BodyPage1[0].S2[0].TextField5[0]': plaintiff_data['zip_code'],
        
        'form1[0].BodyPage1[0].S3[0].t1[0]': defendant_data['address'],
        'form1[0].BodyPage1[0].S3[0].TextField4[0]': defendant_data['apartment_number'],
        'form1[0].BodyPage1[0].S3[0].t2[0]': defendant_data['city'],
        'form1[0].BodyPage1[0].S3[0].TextField4[1]': defendant_data['state'],
        'form1[0].BodyPage1[0].S3[0].TextField5[0]': defendant_data['zip_code'],
        
        'form1[0].BodyPage1[0].S8[0].TextField5[0]': attorney_data['full_name'],
        'form1[0].BodyPage1[0].S8[0].TextField5[4]': attorney_data['address'],
        'form1[0].BodyPage1[0].S8[0].TextField4[0]': attorney_data['apartment_number'],
        'form1[0].BodyPage1[0].S8[0].TextField5[3]': attorney_data['city'],
        'form1[0].BodyPage1[0].S8[0].TextField5[2]': attorney_data['state'],
        'form1[0].BodyPage1[0].S8[0].TextField5[1]': attorney_data['zip_code']
        
    }

    # TODO court and case num
    jud_affidavit_fields = {
        # 'Court': plaintiff_data['court'],
        # 'Case Name and Number if known': plaintiff_data['case_name_and_number'],
        'Name of applicant': plaintiff_data['full_name'],
        'Street and number': plaintiff_data['address'],
        'City or town': plaintiff_data['city'],
        'State and Zip': plaintiff_data['state_and_zip'],
        'Attorney Name': attorney_data['full_name'],
        'Attorney Address': attorney_data['address'],
        'Attorney City': attorney_data['city'],
        'Attorney State and Zip': attorney_data['state_and_zip']
    }

    # TODO add parent 2
    jud_pfc_cjp35_fields = {
        'form1[0].BodyPage1[0].S1[0].TextField4[2]': plaintiff_data['first_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[3]': plaintiff_data['middle_initial'],
        'form1[0].BodyPage1[0].S1[0].TextField4[1]': plaintiff_data['last_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[6]': defendant_data['first_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[4]': defendant_data['last_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[5]': defendant_data['middle_initial'],
        #par 2 thing
            # 'form1[0].BodyPage1[0].S1[0].TextField4[8]': '<def2 mi>',
            # 'form1[0].BodyPage1[0].S1[0].TextField4[9]': '<def2 first name>',
            # 'form1[0].BodyPage1[0].S1[0].TextField4[7]': '<def2 last name>',
        'form1[0].BodyPage1[0].S2[0].TextField4[3]': plaintiff_data['address'],
        'form1[0].BodyPage1[0].S2[0].TextField4[2]': plaintiff_data['apartment_number'],
        'form1[0].BodyPage1[0].S2[0].TextField4[1]': plaintiff_data['city'],
        'form1[0].BodyPage1[0].S2[0].TextField4[0]': plaintiff_data['state'],
        'form1[0].BodyPage1[0].S2[0].TextField5[0]': plaintiff_data['zip_code'],
        
        'form1[0].BodyPage1[0].S3[0].TextField4[1]': plaintiff_data['first_name'],
        'form1[0].BodyPage1[0].S3[0].TextField4[2]': plaintiff_data['middle_initial'],
        'form1[0].BodyPage1[0].S3[0].TextField4[0]': plaintiff_data['last_name'],
        'form1[0].BodyPage1[0].S3[0].TextField4[3]': plaintiff_data['address'],
        'form1[0].BodyPage1[0].S3[0].TextField4[6]': plaintiff_data['apartment_number'],
        'form1[0].BodyPage1[0].S3[0].TextField4[4]': plaintiff_data['city'],
        'form1[0].BodyPage1[0].S3[0].TextField4[5]': plaintiff_data['state'],
        'form1[0].BodyPage1[0].S3[0].TextField5[0]': plaintiff_data['zip_code'],
        
        'form1[0].BodyPage1[0].S4[0].TextField4[1]': defendant_data['middle_initial'],
        'form1[0].BodyPage1[0].S4[0].TextField4[2]': defendant_data['address'],
        'form1[0].BodyPage1[0].S4[0].TextField4[0]': defendant_data['first_name'],
        'form1[0].BodyPage1[0].S4[0].TextField4[3]': defendant_data['city'],
        'form1[0].BodyPage1[0].S4[0].TextField4[6]': defendant_data['last_name'],
        'form1[0].BodyPage1[0].S4[0].TextField4[4]': defendant_data['state'],
        'form1[0].BodyPage1[0].S4[0].TextField4[5]': defendant_data['apartment_number'],
        'form1[0].BodyPage1[0].S4[0].TextField5[0]': defendant_data['zip_code'],
        #par 2 thing
            # 'form1[0].BodyPage2[0].S5[0].TextField4[0]': '<par2 first name>',
            # 'form1[0].BodyPage2[0].S5[0].TextField4[1]': '<par2 mi>',
            # 'form1[0].BodyPage2[0].S5[0].TextField4[6]': '<par2 last name>'
    }
    
    #TODO
    jud_pfc_cjp37_fields = {
        'form1[0].BodyPage1[0].S1[0].TextField4[1]': plaintiff_data['first_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[3]': plaintiff_data['last_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[4]': defendant_data['first_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[6]': defendant_data['last_name'],
        'form1[0].BodyPage1[0].S1[0].TextField4[5]': defendant_data['middle_initial'],
        'form1[0].BodyPage1[0].S1[0].TextField4[7]': defendant_data['address'],
        'form1[0].BodyPage1[0].S1[0].TextField4[8]': defendant_data['city'],
        'form1[0].BodyPage1[0].S1[0].TextField4[9]': defendant_data['state'],
        'form1[0].BodyPage1[0].S1[0].TextField5[1]': defendant_data['zip_code'],
        'form1[0].BodyPage1[0].S1[0].TextField4[10]': attorney_data['full_name']
    }

    #TODO
    notice_of_appearance_fields = {
        'form1[0].BodyPage1[0].CaseNameSub[0].PlffField[0]': plaintiff_data['full_name'],
        'form1[0].BodyPage1[0].CaseNameSub[0].DfdtField[0]': f"{defendant_data['first_name']} {defendant_data['last_name']}",
        'form1[0].BodyPage1[0].AttyField[0]': attorney_data['full_name'],
        'form1[0].BodyPage1[0].AttyAddrField[0]': attorney_data['address'],
        'form1[0].BodyPage1[0].AttyCityField[0]': f"{attorney_data['city']}, {attorney_data['state']} {attorney_data['zip_code']}"
    }

    #TODO
    return {
        'cjd109': cjd109_fields,
        'jud_affidavit': jud_affidavit_fields,
        'jud_pfc_cjp35': jud_pfc_cjp35_fields,
        'jud_pfc_cjp37': jud_pfc_cjp37_fields,
        'notice_of_appearance': notice_of_appearance_fields
    }

def get_names_from_excel(excel_path):
    print(f"Getting names from {excel_path}")
    names = []
    
    data = get_dicts(excel_path)
    
    for row in data:
        names.append(f"{row['Beneficiary First Name']} {row['Beneficiary Middle Name']} {row['Beneficiary Last Name']}")
        
    print(f"Found {len(names)} names")
    return names
    

def process_person_data(row, index):
    first_name = get_field('Beneficiary First Name', row)
    last_name = get_field('Beneficiary Last Name', row)
    
    if first_name == '':
        print(f"ERROR: Row {index+1}: Missing or invalid first name for row {index}")
        return None
    
    if last_name == '':
        print(f"ERROR: Row {index+1}: Missing or invalid last name for row {index}")
        return None
        
    middle_name = get_field('Beneficiary Middle Name', row)
    full_name = f'{first_name} {middle_name} {last_name}'
    beneficiary_name = get_field('Beneficiary Name', row)
    date_opened = get_field('Date Opened', row)
    address_current = get_field('Address-Current', row)
    county = get_field('Address-Current County', row)
    process_type = get_field('Process Type', row)
    age = get_field('Age', row)
    in_care_of = get_field('Address-Current In Care Of', row)
    birth_date = get_field('Birth Date', row)
    nationality = get_field('Nationality', row)
    case_no = get_field('Case No', row)
    i765_receipt_date = get_field('I-765 Receipt Date', row)
    phone_cell = get_field('Phone-Cell', row)
    address = get_field('Address-Current Line 1', row)
    address_line_two = get_field('Address-Current Line 2', row, True)
    address_current_apt = get_field('Address-Current Apt', row, True)
    city = get_field('Address-Current City', row)
    state = get_field('Address-Current State', row)
    zip_code = get_field('Address-Current Zip', row, False, True)
    
    # try:
    #     zip_int = int(row.get('Address-Current Zip', 0))
    #     zip = str(zip_int).zfill(5)
    #     print(f"  Zip: '{zip}'")
    # except:
    #     print(f"ERROR: Row {index+1}: Missing or invalid zip code for {full_name}. Skipping")
    #     zip = ''
    
    try:
        middle_initial = middle_name[0]
    except:
        middle_initial = ""

    # address_line_two_exists = isinstance(address_line_two, str) and not math.isnan(address_line_two)
    # address_current_apt_exists = not isinstance(address_current_apt, str) and not math.isnan(address_current_apt)
    
    # if address_line_two_exists and address_current_apt_exists:
    #     apartment_number = address_current_apt
    # elif not address_current_apt_exists and address_line_two_exists:            
    #     apartment_number = 'N/A'
    # else:
    #     apartment_number = address_line_two if address_line_two_exists else address_current_apt_exists
    #     if isinstance(apartment_number, float):
    #         apartment_number = str(int(apartment_number))
    
    apartment_number = address_current_apt if address_current_apt else address_line_two



    print("\nProcessing completed successfully!")
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
        'middle_initial': middle_initial,
        'full_name': full_name,
        'beneficiary_name': beneficiary_name,
        'address': address,
        'address_current': address_current,
        'apartment_number': apartment_number,
        'city': city,
        'state': state,
        'county': county,
        'zip_code': zip_code,
        'state_and_zip': f'{state} {zip_code}',
        'date_opened': date_opened,
        'process_type': process_type,
        'age': age,
        'in_care_of': in_care_of,
        'birth_date': birth_date,
        'nationality': nationality,
        'case_no': case_no,
        'i765_receipt_date': i765_receipt_date,
        'phone_cell': phone_cell
    }

def get_field(column_header, row, return_NA=False, should_be_num=False):
    value = row.get(column_header, '')
    if not should_be_num and not isinstance(value, str):
        return 'N/A' if return_NA else ''
    elif should_be_num and not isinstance(value, int):
        return 'N/A' if return_NA else ''
    elif isinstance(value, float) and math.isnan(value):
        return 'N/A' if return_NA else ''
    
    return value


def process_forms(excel_path: str, output_dir: str) -> List[str]:
    """Process forms from Excel file and return list of output files"""
    # Define the form files information with correct filenames
    file_info = [
        {
            "name": "cjd109",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/cjd109.pdf"
        },
        {
            "name": "jud_affidavit",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-affidavit-of-indigency-821.pdf"
        },
        {
            "name": "jud_pfc_cjp35",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp35-complaint-for-dependency-c119-s39m.pdf"
        },
        {
            "name": "jud_pfc_cjp37",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp37-judgment-of-dependency-c119-s39m.pdf"
        },
        {
            "name": "notice_of_appearance",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/Notice of Appearance Form - 2023.pdf"
        }
    ]
    
    output_files = []
    
    # Get the data
    plaintiff_data_dicts = get_dicts(excel_path)
    
    # Process each plaintiff
    for index, row in enumerate(plaintiff_data_dicts):
        plaintiff_info = process_person_data(row, index)
        if plaintiff_info is None:
            continue

        # Create output directory
        out_path = os.path.join(output_dir, plaintiff_info["full_name"])
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        # Get form fields and process forms
        form_fields = get_form_fields(plaintiff_info)
        
        for file in file_info:
            try:
                template_path = file["template"]
                if not os.path.exists(template_path):
                    print(f"Template not found: {template_path}")
                    continue
                    
                # Create reader and writer
                reader = PdfReader(template_path)
                writer = PdfWriter()

                # Get the first page
                page = reader.pages[0]
                writer.add_page(page)

                # Update form fields
                writer.update_page_form_field_values(
                    writer.pages[0], form_fields[file["name"]]
                )

                # Save the output file
                output_file = f'{file["name"]}.{plaintiff_info["full_name"]}.pdf'
                output_path = os.path.join(out_path, output_file)
                
                with open(output_path, "wb") as output:
                    writer.write(output)
                
                output_files.append(output_file)
                print(f"Created {output_file}")
                
            except Exception as e:
                print(f"Error processing {file['name']}: {str(e)}")
                
    return output_files

def process_forms_for_client(excel_path: str, output_dir: str, client_name: str) -> List[str]:
    """Process forms for a specific client"""
    # Define the form files information with correct filenames
    file_info = [
        {
            "name": "cjd109",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/cjd109.pdf"
        },
        {
            "name": "jud_affidavit",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-affidavit-of-indigency-821.pdf"
        },
        {
            "name": "jud_pfc_cjp35",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp35-complaint-for-dependency-c119-s39m.pdf"
        },
        {
            "name": "jud_pfc_cjp37",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp37-judgment-of-dependency-c119-s39m.pdf"
        },
        {
            "name": "notice_of_appearance",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/Notice of Appearance Form - 2023.pdf"
        }
    ]
    
    # Get the data
    plaintiff_data_dicts = get_dicts(excel_path)
    
    # Find the client's row
    client_row = None
    for index, row in enumerate(plaintiff_data_dicts):
        full_name = f"{row['Beneficiary First Name']} {row['Beneficiary Middle Name']} {row['Beneficiary Last Name']}"
        if full_name.lower() == client_name.lower():
            client_row = row
            break
    
    if client_row is None:
        raise ValueError(f"Client '{client_name}' not found in the Excel file")
    
    # Process the client's information
    plaintiff_info = process_person_data(client_row, 0)
    if plaintiff_info is None:
        print(f"WARNING: Could not process data for client {client_name}")
        return []

    output_files = []
    
    # Create output directory
    out_path = os.path.join(output_dir, f'{plaintiff_info["full_name"]}v{defendent_info["full_name"]}')
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # Get form fields and process forms
    form_fields = get_form_fields(plaintiff_info)
    
    for file in file_info:
        try:
            template_path = file["template"]
            if not os.path.exists(template_path):
                print(f"Template not found: {template_path}")
                continue
                
            reader = PdfReader(template_path)
            writer = PdfWriter()
            page = reader.pages[0]
            writer.add_page(page)
            writer.update_page_form_field_values(
                writer.pages[0], form_fields[file["name"]]
            )

            output_file = f'{file["name"]}.{plaintiff_info["full_name"]}.pdf'
            output_path = os.path.join(out_path, output_file)
            
            with open(output_path, "wb") as output:
                writer.write(output)
            
            output_files.append(output_file)
            print(f"Created {output_file}")
            
        except Exception as e:
            print(f"Error processing {file['name']}: {str(e)}")
            
    return output_files

def process_forms_for_both(excel_path: str, output_dir: str, plaintiff_name: str, defendant_name: str, attorney_name: str) -> List[str]:
    """Process forms for both plaintiff and defendant"""
    # Define the form files information with correct filenames
    file_info = [
        {
            "name": "cjd109",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/cjd109.pdf"
        },
        {
            "name": "jud_affidavit",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-affidavit-of-indigency-821.pdf"
        },
        {
            "name": "jud_pfc_cjp35",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp35-complaint-for-dependency-c119-s39m.pdf"
        },
        {
            "name": "jud_pfc_cjp37",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/jud-pfc-cjp37-judgment-of-dependency-c119-s39m.pdf"
        },
        {
            "name": "notice_of_appearance",
            "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/templates/Notice of Appearance Form - 2023.pdf"
        }
    ]
    
    # Get the data
    data_dicts = get_dicts(excel_path)
    
    print("=== DEBUG: Names in Excel ===")
    print(f"Looking for plaintiff: {plaintiff_name}")
    print(f"Looking for defendant: {defendant_name}")
    print(f"Looking for attorney: {attorney_name}")
    print("\nNames found in Excel:")
    
    # Find both rows
    plaintiff_row = None
    defendant_row = None
    attorney_row = None
    
    for index, row in enumerate(data_dicts):
        try:
            first_name = row.get('Beneficiary First Name', '')
            middle_name = row.get('Beneficiary Middle Name', '')
            last_name = row.get('Beneficiary Last Name', '')
            full_name = f"{first_name} {middle_name} {last_name}"
            print(f"Row {index}: Name = {full_name}")
            
            # Check for plaintiff match
            if full_name.lower() == plaintiff_name.lower():
                plaintiff_row = row
                print(f"\nFound plaintiff match: {full_name}")
            
            # Check for defendant match
            if full_name.lower() == defendant_name.lower():
                defendant_row = row
                print(f"Found defendant match: {full_name}")
                
            # Check for attorney match
            if full_name.lower() == attorney_name.lower():
                attorney_row = row
                print(f"Found attorney match: {full_name}")
                
        except Exception as e:
            print(f"Error reading row {index}: {str(e)}")
            print(f"Row data: {row}")
    
    print("\n=== Excel Column Names ===")
    if data_dicts and len(data_dicts) > 0:
        print(list(data_dicts[0].keys()))
    else:
        print("No data found in Excel file")
    
    # if plaintiff_row is None:
    #     raise ValueError(f"Plaintiff '{plaintiff_name}' not found in the Excel file")
    # if defendant_row is None:
    #     raise ValueError(f"Defendant '{defendant_name}' not found in the Excel file")
    
    # Process all three parties using the same function
    plaintiff_info = process_person_data(plaintiff_row, 0)
    if plaintiff_info is None:
        print(f"WARNING: Could not process data for defendant '{plaintiff_name}'")
        
    defendant_info = process_person_data(defendant_row, 1)
    if defendant_info is None:
        print(f"WARNING: Could not process data for defendant '{defendant_name}'")
        
    attorney_info = process_person_data(attorney_row, 2)
    if attorney_info is None:
        print(f"WARNING: Could not process data for defendant '{attorney_name}'")
    
    # Get form fields with all three data sets
    form_fields = get_form_fields(plaintiff_info, defendant_info, attorney_info)
    
    output_files = []
    out_path = os.path.join(output_dir, plaintiff_info["full_name"])
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    
    for file in file_info:
        try:
            template_path = file["template"]
            if not os.path.exists(template_path):
                print(f"Template not found: {template_path}")
                continue
                
            reader = PdfReader(template_path)
            writer = PdfWriter()
            page = reader.pages[0]
            writer.add_page(page)
            writer.update_page_form_field_values(
                writer.pages[0], form_fields[file["name"]]
            )

            output_file = f'{file["name"]}.{plaintiff_info["full_name"]}.pdf'
            output_path = os.path.join(out_path, output_file)
            
            with open(output_path, "wb") as output:
                writer.write(output)
            
            output_files.append(output_file)
            print(f"Created {output_file}")
            
        except Exception as e:
            print(f"Error processing {file['name']}: {str(e)}")
            
    return output_files

if __name__ == "__main__":
    main()

