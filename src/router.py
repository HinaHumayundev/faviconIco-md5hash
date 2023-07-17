from fastapi import APIRouter
from pydantic import BaseModel
import ipaddress
import logging
import asyncio
from utils import get_cleaned_dict_from_xml, get_md5, match_md5_with_data

router = APIRouter()


class IPAddressRequest(BaseModel):
    ip_addresses: list[str]


@router.post("/md5-matching")
async def match_md5_with_ip_addresses(request: IPAddressRequest):
    """
    Matches MD5 hash values with IP addresses and retrieves corresponding data.

    Args:
        request (IPAddressRequest): The request containing a list of IP addresses.

    Returns:
        dict: A dictionary containing the matched data for each IP address.
    """
    ip_addresses = request.ip_addresses
    ip_addresses = list(set(ip_addresses))
    data = await get_cleaned_dict_from_xml("favicons.xml")

    tasks = []
    for ip in ip_addresses:
        if "-" in ip:
            ip_range = ip.split("-")
            try:
                start_ip = ipaddress.ip_address(ip_range[0])
                end_ip = ipaddress.ip_address(ip_range[1])
            except ValueError:
                logging.error(f"{ip} is an invalid IP address range")
                continue

            ip_list = [str(ip) for ip in ipaddress.summarize_address_range(start_ip, end_ip)]
            tasks.extend(get_md5(ip) for ip in ip_list)
        else:
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                logging.error(f"{ip} is an invalid IP address")
                continue
            tasks.append(get_md5(ip))

    md5s = await asyncio.gather(*tasks)
    md5s = [elem for elem in md5s if elem is not None]

    tasks.clear()

    for md5 in md5s:
        tasks.append(match_md5_with_data(md5, data))

    matched_data = await asyncio.gather(*tasks)
    matched_data = [elem for elem in matched_data if elem is not None]
    return {"matched_data": matched_data}
