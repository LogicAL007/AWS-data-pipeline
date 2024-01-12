import os
import pandas as pd
import requests
from dotenv import load_dotenv


def send_json_data(customers_data, URL):
    """
    Send customer data as JSON to an API endpoint.

    :param URL: this API address for the post request
    :param customers_data: DataFrame containing customer data.

    Raises:
    Exception: If there's an error while sending data to the API.

    Returns:
    None
    """
    for i in customers_data.index:
        try:
            # convert the row to json
            export = customers_data.loc[i].to_json()

            # send it to the API
            response = requests.post(URL, data=export)

            # print the return code and response content
            print(f"The response below has been sent to the API_URL (Status Code: {response.status_code})")
            print(export)
            print(response.text)
        except Exception as e:
            print(f"Error sending data for row {i}: {str(e)}")


def main():
    load_dotenv()
    URL = os.getenv("API_URL")
    FILE_PATH = os.getenv('CSV_PATH')
    customer_data = pd.read_csv(FILE_PATH)

    send_json_data(customer_data, URL)


if __name__ == '__main__':
    main()
