# To use for local machine: 
# - Rename google_sheet_url for your own personal Google Sheet, making sure the Sheet is shared publically (not private). 
#   The Sheet can be made by going to the year's IEEE site, click export (make sure you have no selections so it can send a 1,000 file .csv), and then importing it to Google Sheets.
#   Then rename the google_sheet_url the same just change the "1D5DEnD0hrBwWdwOndquRh_DVe-Ml03l67z9EDOkrRaw" to your personal url.
# - Rename directory to your own local machine path.

import os
import pandas as pd
import re

# Function to sanitize file names
def sanitize_filename(name):
    if not isinstance(name, str):  # Ensure the input is a string
        name = str(name) if pd.notna(name) else ''  # Convert non-NaN values to strings; replace NaN with an empty string
    # Replace parentheses and their content with a space
    name = re.sub(r'\(.*?\)', ' ', name)  # Replace (content) with a space
    # Replace slashes and dashes with a single space
    name = re.sub(r'[/-]', ' ', name)
    # Remove invalid characters for Windows file names, but preserve commas and apostrophes
    name = re.sub(r'[<>:"\\|?*]', '', name)  # Do not remove ',' or "'"
    # Normalize whitespace (strip leading/trailing spaces and replace multiple spaces with one)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# Step 1: Load Google Sheets data
google_sheet_url = "https://docs.google.com/spreadsheets/d/1D5DEnD0hrBwWdwOndquRh_DVe-Ml03l67z9EDOkrRaw/export?format=csv"
sheet_data = pd.read_csv(google_sheet_url)

# Step 2: Add a row number column to the DataFrame
sheet_data = sheet_data.reset_index()
sheet_data.rename(columns={'index': 'RowNumber'}, inplace=True)

# Sanitize document titles in the CSV
sheet_data['SanitizedTitle'] = sheet_data['Document Title'].apply(sanitize_filename)

# Step 3: List files in directory
directory = r"C:\Users\mateo\..." # Update as needed
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Step 4: Match and rename files
for file_name in files:
    # Remove the .pdf extension for matching
    base_name = os.path.splitext(file_name)[0]

    # Sanitize the base name of the file for matching
    sanitized_base_name = sanitize_filename(base_name)

    # Match with sanitized titles in Google Sheets data
    match = sheet_data[sheet_data['SanitizedTitle'] == sanitized_base_name]
    if not match.empty:
        year = match['Publication Year'].values[0]  # Replace 'Year' with actual column name if different
        row_number = match['RowNumber'].values[0] + 1  # Add 1 to make it start from 1 instead of 0
        new_name = f"{year}-{row_number}. {file_name}"  # Keep original file extension

        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {file_name} -> {new_name}")
    else:
        print(f"No match found for: {file_name}")
