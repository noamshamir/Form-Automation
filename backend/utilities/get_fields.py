from PyPDF2 import PdfReader

# List of file templates
file_info = [
    {
        "name": "cjd109",
        "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/cjd109.pdf"
    },
    {
        "name": "jud_affidavit",
        "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/jud-affidavit-of-indigency-821.pdf"
    },
    {
        "name": "jud_pfc_cjp35",
        "template": "/Users/noamshamir/Documents/Mabel/Form Automation/in/jud-pfc-cjp35-complaint-for-dependency-c119-s39m.pdf"
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

def get_fields(file_path):
    reader = PdfReader(file_path)
    fields = reader.get_fields()
    return fields

# Loop through the files and print '/T' and '/TU' values
for file in file_info:
    print()
    print()
    print()
    print()
    print()
    print("--------------------------------")
    print()
    print()
    print()
    print()
    print()

    print(file)
    fields = get_fields(file["template"])
    for field_name, field_attributes in fields.items():
        t_value = field_attributes.get('/T', 'N/A')
        tu_value = field_attributes.get('/DV', 'N/A')
        if tu_value != 'N/A' and tu_value:
            print(f"'{t_value}': '{tu_value}',")