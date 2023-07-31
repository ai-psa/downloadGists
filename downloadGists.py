#!/usr/bin/env python3

# Import necessary libraries
import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import argparse
import json

# Print a note about GitHub API rate limit
print("Please note that the GitHub API has a rate limit. For more information, visit https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting")

# Function to download all gists from a user
def download_all_from_user(user: str, extension: str, token: str = None, timeframe_created: str = None, timeframe_updated: str = None, overwrite: bool = False, filename: str = None):
    # Initialize counters for files
    total_files_reviewed = 0
    total_files_downloaded = 0
    total_files_overwritten = 0  # Initialize counter for overwritten files
    total_files_skipped = 0
    
    headers = {"Accept": "application/vnd.github+json"} # Set headers for the request
    # If token is provided, add it to the headers
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Convert timeframe to datetime object
    if timeframe_created:
        try:
            # Check the length of the input to determine the format
            if len(timeframe_created) == 4:  # YYYY
                timeframe_created = datetime.strptime(timeframe_created, '%Y')
            elif len(timeframe_created) == 7:  # YYYY-MM
                timeframe_created = datetime.strptime(timeframe_created, '%Y-%m')
            elif len(timeframe_created) == 10:  # YYYY-MM-DD
                timeframe_created = datetime.strptime(timeframe_created, '%Y-%m-%d')
            # Ignore the time part
            timeframe_created = timeframe_created.replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            # If the format is incorrect, print an error message and return
            print("Invalid format for timeframe_created. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")
            return
    if timeframe_updated:
        try:
            # Check the length of the input to determine the format
            if len(timeframe_updated) == 4:  # YYYY
                timeframe_updated = datetime.strptime(timeframe_updated, '%Y')
            elif len(timeframe_updated) == 7:  # YYYY-MM
                timeframe_updated = datetime.strptime(timeframe_updated, '%Y-%m')
            elif len(timeframe_updated) == 10:  # YYYY-MM-DD
                timeframe_updated = datetime.strptime(timeframe_updated, '%Y-%m-%d')
            # Ignore the time part
            timeframe_updated = timeframe_updated.replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            # If the format is incorrect, print an error message and return
            print("Invalid format for timeframe_updated. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")
            return
    # Initialize variables for pagination
    next_page = True
    page = 1
    
    # Loop until there are no more pages of gists
    while next_page:
        # Construct the URL for the current page of gists
        url = f"https://api.github.com/users/{user}/gists?page={page}"
    
        # Make a GET request to the GitHub API
        response = requests.get(url, headers=headers)

        # If the response is empty, there are no more pages of gists
        if not response.json():
            next_page = False
        # Otherwise, increment the page number and continue to the next page
        else:
            page += 1
        # Call the function to download all gists from the response
        try:
            response_data = response.json()
            if isinstance(response_data, list):
                for gist in response_data:
                    if isinstance(gist, dict):  # Ensure that gist is a dictionary
                        downloaded, skipped, overwritten = download(gist, extension, timeframe_created, timeframe_updated, overwrite, filename)
                        total_files_downloaded += downloaded
                        total_files_skipped += skipped
                        total_files_overwritten += overwritten
                        total_files_reviewed += len(gist['files'])  # Increment the counter for each file in the gist
        except Exception as e:
            print(f"An error occurred while downloading gists: {e}")
            if str(e) == "string indices must be integers":
                print("Please ensure that the response from the GitHub API is a JSON array of gists.")
            return  # Corrected indentation
   
  
    # Calculate percentage of files downloaded
    percent_downloaded = (total_files_downloaded / total_files_reviewed) * 100 if total_files_reviewed > 0 else 0
      
    # Print totals
    print(f"# of files reviewed: {total_files_reviewed}")
    print(f"# of files skipped: {total_files_skipped}")
    print(f"# of files downloaded: {total_files_downloaded}")
    print(f"% of files downloaded: {percent_downloaded:.2f}%")
    print(f"# of files overwritten: {total_files_overwritten}")
    return total_files_reviewed, total_files_downloaded, total_files_skipped, total_files_overwritten

def download_all(gists: list):
    with PoolExecutor(max_workers=10) as executor:
        for _ in executor.map(download, gists):
            pass
        
# Function to download a single gist
def download(gist, extension, timeframe_created, timeframe_updated, overwrite, filename: str = None):
    # Initialize counters
    total_files_downloaded = 0
    total_files_overwritten = 0  # Initialize counter for overwritten files
    total_files_skipped = 0  # Initialize counter for skipped files
    target = "gists"
    
    # Create the directory if it doesn't exist
    if not os.path.exists(target):
        os.makedirs(target)
    
    # Download each file in the gist that matches the extension
    for file_info in gist['files'].values():
        print(f"Reviewing file: {file_info['filename']}")  # Print the filename of the file being reviewed
        # If filename is provided and it's not in the file's name, skip this file
        if filename and filename not in file_info['filename']:
            total_files_skipped += 1  # Increment the counter for skipped files
            continue
        # If extension is provided and it's not in the file's name, skip this file
        if extension is None or extension == '*' or file_info['filename'].endswith(extension):
            # Convert the creation and update times to datetime objects
            created_at = datetime.strptime(gist['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(hour=0, minute=0, second=0, microsecond=0)
            updated_at = datetime.strptime(gist['updated_at'], '%Y-%m-%dT%H:%M:%SZ').replace(hour=0, minute=0, second=0, microsecond=0)
            # If timeframe_created is provided and the file was created before it, skip this file
            if timeframe_created and created_at < timeframe_created:
                total_files_skipped += 1  # Increment the counter for skipped files
                continue
            # If timeframe_updated is provided and the file was updated before it, skip this file
            if timeframe_updated and updated_at < timeframe_updated:
                total_files_skipped += 1  # Increment the counter for skipped files
                continue
            # Get the raw URL of the .md file
            raw_url = file_info['raw_url']
            # Try to download the .md file
            try:
                response = requests.get(raw_url)
                # If the request fails, raise an exception
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                # Print the error and skip this file
                print(f"An error occurred: {e}")
                total_files_skipped += 1  # Increment the counter for skipped files
                continue
            # Write the content of the .md file to a local file
            file_path = os.path.join(target, file_info['filename'])
            # If overwrite is not provided and the file already exists, skip this file
            if not overwrite and os.path.exists(file_path):
                print(f"File {file_path} already exists, skipping.")
                total_files_skipped += 1  # Increment the counter for skipped files
                continue
            elif overwrite and os.path.exists(file_path):
                total_files_overwritten += 1  # Increment the counter for overwritten files
            # Increment the counter for downloaded files
            total_files_downloaded += 1
            # Open the file in write mode and write the content
            with open(file_path, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
                f.write(response.text)
    return total_files_downloaded, total_files_skipped, total_files_overwritten


    # Append the gist's description and metadata to a single file in the common directory
    description_file = os.path.join(target, "_descriptions.txt")
    # Open the file in append mode and write the description
    with open(description_file, "a", encoding='utf-8') as f:  # Specify UTF-8 encoding
        f.write(f"Gist ID: {gist['id']}\nCreated at: {gist['created_at']}\nUpdated at: {gist['updated_at']}\nFilename: {file_info['filename']}\nDescription: {gist['description']}\n\n")  # Add a newline character after each description
if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Download gists from a GitHub user.")


    # Add the arguments
    parser.add_argument("user", type=str, help="The GitHub username.")
    parser.add_argument("--token", type=str, help="The GitHub access token. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token for more information.")
    parser.add_argument('--extension', type=str, default=None, help='File extension to download. Defaults to all files if not provided.')
    parser.add_argument('--timeframe_created', type=str, help='Filter gists based on when they were created. Provide date in the format: YYYY, YYYY-MM, or YYYY-MM-DD')
    parser.add_argument('--timeframe_updated', type=str, help='Filter gists based on when they were updated. Provide date in the format: YYYY, YYYY-MM, or YYYY-MM-DD')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files. If not provided, existing files will be skipped.')
    parser.add_argument('--filename', type=str, help='Download files whose filename contains this string.')
    

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    download_all_from_user(args.user, args.extension, args.token, args.timeframe_created, args.timeframe_updated, args.overwrite, args.filename)

