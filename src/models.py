from pydantic import BaseModel


class IPAddressRequest(BaseModel):
    """
    Represents a request containing a list of IP addresses.
    """

    ip_addresses: list[str]
