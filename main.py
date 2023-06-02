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


if __name__ == "__main__":
    # The url consists of the raw json data of all timezones
    url = "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
    # creating object for the TimezoneDataDownloader class
    downloader = TimezoneDataDownloader(url,offset=5.5)
    # calling the object to fetch the data in the required manner
    data = downloader.download_data()
    print(data)
