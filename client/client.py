import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()


URL = os.getenv("API_URL")
FILE_PATH = os.getenv('CSV_PATH')

# read the testfile
customer_data = pd.read_csv(FILE_PATH)

def send_json_data(customer_data):
    for i in customer_data.index:
        try:
            # convert the row to json
            export = customer_data.loc[i].to_json()

            # send it to the api
            response = requests.post(URL, data=export)

            # print the return code and response content
            print(f"The response below has been sent to the API_URL (Status Code: {response.status_code})")
            print(export)
            print(response.text)
        except Exception as e:
            print(f"Error sending data for row {i}: {str(e)}")

if __name__ == '__main__':
    send_json_data(customer_data)
