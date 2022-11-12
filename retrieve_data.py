"""
Class for getting the data from the feed
"""
import requests
from feed_processer import Feed_Processor


class Retrieve_Data:

    def __init__(self, feed_url):
        """
        Constructor for the class
        url: url of the feed
        """
        self.feed_url = feed_url

    def get_data(self, params=None):
        """
        Get the data from the feed
        :return: dictionary of the feed data
        """
        # Get the data from the feed
        try:
            response = requests.get(self.feed_url, params=params)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        # Check the status code
        if response.status_code != 200:
            raise ValueError("Error: " + str(response.status_code))
        # Get the data
        data = response.text
        # Check the type of the feed
        if data[0] == "{" or data[0] == "[":
            data_type = "json"
        elif data[0] == "<":
            data_type = "xml"
        else:
            raise ValueError("Error: Invalid feed type!")
        # Process the data
        feed_processor = Feed_Processor(data, data_type)
        feed_dict = feed_processor.data_to_dict()
        return feed_dict