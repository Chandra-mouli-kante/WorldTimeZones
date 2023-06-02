import requests
import json
import pandas as pd


class TimezoneDataDownloader:
    def __init__(self, url, **params):
        self.url = url
        self.match = None
        self.offset = None
        if "match" in params.keys():
            self.match = params["match"]
        if "offset" in params.keys():
            self.offset = params["offset"]

    def desired_output(func):
        def wrapper(*args):
            result = func(*args)
            # checks whether there is any data in the dataframe received
            if result["value"].size > 0 and (result is not None):
                return result
            else:
                return "No timezone found for the given offset or name"

        return wrapper

    @desired_output
    def download_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            # converting JSON string to python object
            json_data = json.loads(response.text)
            # converting the python object into table using pandas library
            df = pd.DataFrame(json_data)
            # checking for the input of the optional parameters
            if self.match is not None:
                return df[df["value"] == self.match]
            elif self.offset is not None:
                return df[df["offset"] == self.offset]
            else:
                # returns the entire table if no optional parameters are given
                return df
        else:
            return None


def getTimesZonesData():
    # The url consists of the raw json data of all timezones
    url = "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
    # input
    input_type = input("Enter the type of input 'match' or 'offset' or 'getAll' :")
    if input_type == "match":
        match = input("Enter the value for match: ")
        # creating object for the TimezoneDataDownloader class
        downloader = TimezoneDataDownloader(url, match=match)
        # calling the object to fetch the data in the required manner
        data = downloader.download_data()
        print(data)
    elif input_type == "offset":
        offset = int(input("Enter the value for offset: "))
        # creating object for the TimezoneDataDownloader class
        downloader = TimezoneDataDownloader(url, offset=offset)
        # calling the object to fetch the data in the required manner
        data = downloader.download_data()
        print(data)
    elif input_type == "getAll":
        # creating object for the TimezoneDataDownloader class
        downloader = TimezoneDataDownloader(url)
        # calling the object to fetch the data in the required manner
        data = downloader.download_data()
        print(data)
    else:
        raise Exception()


if __name__ == "__main__":
    try:
        # print("The user can query timezones data here")
        # print("User can opt for specific queries like match or offset or getAll times zones")
        # print("The inputs given for the match and offset should be precise")
        # print("An application by Chandra")
        #calling the method to fetch the timezones data
        getTimesZonesData()
    except:
        print("Please enter your query in correct format")
        getTimesZonesData()
