from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from pathlib import Path
import uuid
import sys
import traceback
import pandas as pd
from typing import List

try:
    from form_automator import process_forms_for_both, get_names_from_excel
    print("Successfully imported form_automator")
except Exception as e:
    print(f"Error importing form_automator: {str(e)}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    raise

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use your existing directories
IN_DIR = Path("../in")
OUT_DIR = Path("../out")
IN_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

def combine_excel_files(file_paths: List[str]) -> str:
    """Combine multiple Excel files into one"""
    print(f"Starting to combine Excel files from paths: {file_paths}")
    dfs = []
    for file_path in file_paths:
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_path = str(IN_DIR / f"combined_{uuid.uuid4()}.xlsx")
    print(f"Saving combined Excel file to: {combined_path}")
    combined_df.to_excel(combined_path, index=False)
    return combined_path

@app.post("/api/process-forms")
async def process_excel_files(
    excel_files: List[UploadFile] = File(...),
    plaintiff_name: str = Form(...),
    defendant_name: str = Form(...),
    attorney_name: str = Form(...)
) -> dict:
    try:
        print(f"\n=== Starting new form processing request ===")
        print(f"Received {len(excel_files)} files")
        print(f"Plaintiff: {plaintiff_name}")
        print(f"Defendant: {defendant_name}")
        print(f"Attorney: {attorney_name}")
        
        # Save all uploaded files
        temp_paths = []
        for excel_file in excel_files:
            temp_path = IN_DIR / f"temp_{uuid.uuid4()}_{excel_file.filename}"
            print(f"Saving uploaded file {excel_file.filename} to {temp_path}")
            
            with temp_path.open("wb") as buffer:
                content = await excel_file.read()
                buffer.write(content)
            
            temp_paths.append(str(temp_path))
        
        try:
            # Combine Excel files
            print("\n=== Combining Excel files ===")
            combined_path = combine_excel_files(temp_paths)
            print(f"Combined file saved at: {combined_path}")
            
            # Process the combined file
            print("\n=== Calling process_forms_for_both ===")
            print(f"Input file: {combined_path}")
            print(f"Output directory: {OUT_DIR}")
            print(f"Names: {plaintiff_name}, {defendant_name}, {attorney_name}")
            
            # Print the absolute paths for debugging
            print(f"Absolute input path: {os.path.abspath(combined_path)}")
            print(f"Absolute output path: {os.path.abspath(str(OUT_DIR))}")
            
            output_files = process_forms_for_both(
                combined_path, 
                str(OUT_DIR),
                plaintiff_name,
                defendant_name,
                attorney_name
            )
            
            # Modify the output files to include the person's directory
            output_files = [f"{plaintiff_name}/{file}" for file in output_files]
            
            print("\n=== Process completed ===")
            print(f"Generated output files: {output_files}")
            
            # Verify files exist
            for file in output_files:
                file_path = OUT_DIR / file
                if not file_path.exists():
                    print(f"WARNING: Generated file does not exist: {file_path}")
                else:
                    print(f"Verified file exists: {file_path}")
                    print(f"File size: {os.path.getsize(file_path)} bytes")
                    print(f"File type: {os.path.splitext(file)[1]}")
            
            # Clean up temp files
            print("\n=== Cleaning up temporary files ===")
            for temp_path in temp_paths:
                os.remove(temp_path)
                print(f"Removed temp file: {temp_path}")
            os.remove(combined_path)
            print(f"Removed combined file: {combined_path}")
            
            return {"files": output_files}
            
        except Exception as process_error:
            print(f"\n=== Error in processing ===")
            print(f"Error type: {type(process_error)}")
            print(f"Error message: {str(process_error)}")
            print("Full traceback:")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Error processing files: {str(process_error)}"
            )
            
    except Exception as e:
        print(f"\n=== Unexpected error ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading files: {str(e)}"
        )

@app.post("/api/names")
async def get_names(excel_files: List[UploadFile] = File(...)) -> dict:
    try:
        temp_paths = []
        for excel_file in excel_files:
            temp_path = IN_DIR / f"temp_{uuid.uuid4()}_{excel_file.filename}"
            print(f"Saving uploaded file {excel_file.filename} to {temp_path}")
            
            with temp_path.open("wb") as buffer:
                content = await excel_file.read()
                buffer.write(content)
            
            temp_paths.append(str(temp_path))
            print(f"Temp paths: {temp_paths}")
            
            combined_path = combine_excel_files(temp_paths)
            
            names = get_names_from_excel(combined_path)
            print(f"Names: {names}")
            
            return {"names": names}
            
            
    finally:
        for temp_path in temp_paths:
            os.remove(temp_path)
            print(f"Removed temp file: {temp_path}")
        
    return {"result": "success"}

@app.get("/api/download/{full_path:path}")
async def download_file(full_path: str):
    print(f"\n=== Download request for path: {full_path} ===")
    
    # Construct the full file path
    file_path = OUT_DIR / full_path
    print(f"Looking for file at: {file_path}")
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        print("Contents of OUT_DIR:")
        for root, dirs, files in os.walk(OUT_DIR):
            print(f"\nDirectory: {root}")
            for d in dirs:
                print(f"  Dir: {d}")
            for f in files:
                print(f"  File: {f}")
                
        raise HTTPException(
            status_code=404, 
            detail=f"File not found: {full_path}"
        )
    
    try:
        print(f"File exists, size: {os.path.getsize(file_path)} bytes")
        print(f"File type: {os.path.splitext(full_path)[1]}")
        
        return FileResponse(
            path=file_path,
            filename=full_path.split('/')[-1],  # Use just the filename part for download
            media_type='application/pdf'
        )
    except Exception as e:
        print(f"\n=== Error serving file ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error serving file: {str(e)}"
        )

@app.get("/api/test")
async def test_endpoint():
    return {"message": "Backend is working"}

if __name__ == "__main__":
    print("\n=== Starting FastAPI server ===")
    print(f"Input directory: {IN_DIR}")
    print(f"Output directory: {OUT_DIR}")
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=3001,
        reload=True
    )