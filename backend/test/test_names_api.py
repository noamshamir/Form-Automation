import requests
import os
from pathlib import Path

def test_names_endpoint():
    # URL of your FastAPI endpoint
    url = 'http://localhost:3000/api/names'
    
    # Path to your test Excel file(s)
    test_files_dir = Path('../../in')  # Adjust this path as needed
    
    # Find all Excel files in the directory
    excel_files = []
    for file in test_files_dir.glob('*.xlsx'):
        if file.name == 'excel_test.xlsx':
            excel_files.append(('excel_files', (file.name, open(file, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')))
    
    if not excel_files:
        print("No Excel files found in the specified directory!")
        return
    
    try:
        # Make the POST request
        print(f"Sending request to {url} with {len(excel_files)} files...")
        for file in excel_files:
            print(f"File: {file[1][0]}")
            
        response = requests.post(url, files=excel_files)
        
        # Check the response
        if response.status_code == 200:
            print("\nSuccess!")
            print("Names found:")
            for name in response.json()['names']:
                print(f"- {name}")
        else:
            print(f"\nError: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\nError making request: {str(e)}")
        
    finally:
        # Close all file handles
        for file in excel_files:
            file[1][1].close()

if __name__ == "__main__":
    test_names_endpoint() 