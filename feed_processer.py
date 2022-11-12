"""
Class for processing the RSS feed into the different types.
Author: Jiacheng Zhao (John)
Date: 11/12/22
"""
from bs4 import BeautifulSoup
import json


class Feed_Processor:
    """
    Parser class
    """

    def __init__(self, feed_raw_data, data_type):
        """
        Constructor for the class, takes the raw data and the type of the feed
        feed_raw_data: raw data of the feed
        data_type: type of the feed
        """
        self.feed_raw_data = feed_raw_data
        self.type = data_type
        # Check if the feed is RSS3 based on the type
        if data_type == "json":
            self.feed_data = json.loads(feed_raw_data)
        elif data_type == "xml":
            self.feed_data = BeautifulSoup(self.feed_raw_data, 'xml')
        else:
            raise ValueError("Invalid feed type! Only json and xml are supported.")

    def data_to_dict(self):
        """
        Convert the feed data to a dictionary
        :return: dictionary of the feed data
        """
        # Check if the feed is RSS3 based on the type
        if self.type == "json":
            # Check if the feed contains the error message
            if "error" in self.feed_data:
                raise ValueError("Error: " + self.feed_data["error"])
            feed_dict = {"rss_version": '3.0'}
            # Get the result
            result = self.feed_data["result"]
            feed_dict["data"] = []
            # Loop through the result
            for item in result:
                title = item["hash"]
                # Check the type of the item
                success = item["success"]
                if success:
                    success_str = "successfully"
                else:
                    success_str = "failed to"
                if item["type"] == "burn":
                    # Check the action of the item
                    burned_count = 0
                    minted_count = 0
                    for action in item["actions"]:
                        if action["type"] == "burn":
                            burned_count += 1
                        elif action["type"] == "mint":
                            minted_count += 1
                    # Set the title
                    description = item["owner"] + " " + success_str + " burn " + str(burned_count) + " NFTs"
                    if minted_count > 0:
                        description += " and minted " + str(minted_count) + " NFTs"
                    description += " on " + item["network"] + " with fee " + str(item["fee"])
                elif item["type"] == "mint":
                    description = item["owner"] + " " + success_str + " minted " + str(len(item["actions"])) + \
                                  " NFT(s) on " + item["network"] + " with fee " + str(item["fee"])
                elif item["type"] == "transfer":
                    description = item["address_from"] + " " + success_str + " transferred " + \
                                  str(len(item["actions"])) + " NFT(s) to " + item["address_to"] + " on " + \
                                  item["network"] + " with fee " + str(item["fee"])
                else:
                    description = "Unknown action, please check the transaction on the explorer"
                # Check the network, to determine the explorer
                if item["network"] == "ethereum":
                    explorer = "https://etherscan.io/tx/"
                elif item["network"] == "polygon":
                    explorer = "https://polygonscan.com/tx/"
                elif item["network"] == "bsc":
                    explorer = "https://bscscan.com/tx/"
                else:
                    explorer = None
                # Add the item to the dictionary
                if explorer is not None:
                    feed_dict["data"].append(
                        {
                            "title": title,
                            "description": description,
                            "link": explorer + item["hash"],
                            "timestamp": item["timestamp"],
                            "dump": str(item)
                        }
                    )
                else:
                    feed_dict["data"].append(
                        {
                            "title": title,
                            "description": description,
                            "timestamp": item["timestamp"],
                            "dump": str(item)
                        }
                    )
            return feed_dict
        else:
            if self.feed_data.find("rss") is None:
                feed_dict = {"rss_version": '1.0'}
            else:
                feed_dict = {"rss_version": '2.0'}
            # Get the version of the feed
            # Based on the version, get the feed data
            if feed_dict['rss_version'] == '1.0':
                feed = self.feed_data.find("feed")
                feed_dict['channel_title'] = feed.find('title').text
                feed_dict['channel_link'] = feed.find('link').text
                feed_dict["data"] = []
                for item in feed.findAll('entry'):
                    feed_dict["data"].append(
                        {
                            'title': item.find('title').text,
                            'link': item.find('link').text,
                            'content': item.find('content').text,
                            'timestamp': item.find('published').text,
                            'dump': str(item)
                        }
                    )
            elif feed_dict['rss_version'] == '2.0':
                channel = self.feed_data.find('channel')
                feed_dict['channel_title'] = channel.find('title').text
                feed_dict['channel_link'] = channel.find('link').text
                feed_dict['channel_description'] = channel.find('description').text
                feed_dict["data"] = []
                for item in channel.findAll('item'):
                    if item.find('pubDate') is None:
                        timestamp = None
                    else:
                        timestamp = item.find('pubDate').text
                    feed_dict["data"].append(
                        {
                            'title': item.find('title').text,
                            'description': item.find('description').text,
                            'link': item.find('link').text,
                            'timestamp': timestamp,
                            'dump': str(item)
                        }
                    )
            return feed_dict
