import hashlib
import xmltodict
import aiohttp
from bs4 import BeautifulSoup
import socket
import os
import re


async def get_cleaned_dict_from_xml(file_name):
    """
    Parses an XML file and extracts relevant data into a cleaned dictionary.

    Args:
        file_name (str): The name of the XML file to parse.

    Returns:
        dict: A dictionary containing cleaned data extracted from the XML.
    """

    cleaned_data = dict()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    with open(file_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    for element in data_dict['fingerprints']['fingerprint']:
        cleaned_data[element['@pattern']] = element

    return cleaned_data


async def match_md5_with_data(md5, data):
    """
    Matches an MD5 hash with the corresponding data in the provided dictionary.

    Args:
        md5 (str): The MD5 hash value to match.
        data (dict): A dictionary containing the data to search.

    Returns:
        dict: The matched data if a match is found, otherwise None.
    """
    for item in data.keys():
        matched_data = re.search(item, md5)
        if matched_data:
            return data[item]


async def get_md5(ip_address):
    """
    Retrieves the MD5 hash value of a favicon from a given IP address.

    Args:
        ip_address (str): The IP address to fetch the favicon from.

    Returns:
        str: The MD5 hash value of the favicon content, or None if an error occurs.
    """
    try:
        icon_ref = await get_favicon(ip_address)
    except Exception as e:
        try:
            icon_ref = await get_favicon(ip_address, use_https=True)
        except Exception as ee:
            return

    try:
        fav_icon_url = f"http://{ip_address}/{icon_ref}"
        fav_icon_url = fav_icon_url.replace("\\", "/")

        async with aiohttp.ClientSession() as session:
            async with session.get(fav_icon_url) as favicon_response:
                favicon_content = await favicon_response.read()

        favicon_md5 = hashlib.md5(favicon_content).hexdigest()
        return favicon_md5
    except Exception as e:
        return


async def get_favicon(domain, use_https=False):
    """
    Retrieves the URL of a website's favicon.

    Args:
        domain (str): The domain or IP address of the website.
        use_https (bool, optional): Whether to use HTTPS when fetching the favicon URL. Defaults to False.

    Returns:
        str: The URL of the favicon, or None if it cannot be found.
    """
    if use_https:
        domain = socket.getnameinfo((domain, 0), 0)[0]

    if 'http' not in domain:
        domain = 'http://' + domain

    async with aiohttp.ClientSession() as session:
        async with session.get(domain) as response:
            if response.status == 200:
                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                icon_link = soup.find("link", rel="shortcut icon")
                if icon_link is None:
                    icon_link = soup.find("link", rel="icon")
                if icon_link is None:
                    return domain + '/favicon.ico'
                return icon_link["href"]
