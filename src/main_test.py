import pytest
import logging
from fastapi.testclient import TestClient
from main import app
from utils import match_md5_with_data


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "ip_addresses, expected_matched_count",
    [
        (["185.182.56.42"], 1),  # Single IP address
        (["185.182.56.42", "185.182.56.42"], 1),  # Test with Duplicate Values
        (["134.209.150.228", "192.168.0.1-192.168.0.4", "185.182.56.42"], 1),
        # Test with the combination of IP addresses and IP address ranges in - notation
        (["6.A.34.2", "185.182.56.42"], 1),  # Test with an invalid IP address
    ]
)
def test_md5_matching(client, ip_addresses, expected_matched_count):
    """
    Test the MD5 matching endpoint with various IP addresses and expected matched count.

    """
    payload = {"ip_addresses": ip_addresses}
    response = client.post("/md5-matching", json=payload)

    # Verify the response status code and the presence of "matched_data" in the response JSON
    assert response.status_code == 200
    assert "matched_data" in response.json()

    matched_data = response.json()["matched_data"]

    print(f"IP addresses: {ip_addresses}")
    print(f"Expected matched count: {expected_matched_count}")
    print(f"Actual matched count: {len(matched_data)}")
    print(f"Matched data: {matched_data}")

    # Verify the length of matched_data matches the expected_matched_count
    assert len(matched_data) == expected_matched_count

    if "invalid-ip-address" in ip_addresses:
        # Verify that an error message is logged for the invalid IP address
        assert logging.error.called
        logged_message = logging.error.call_args[0][0]
        assert "invalid-ip-address" in logged_message


@pytest.mark.asyncio
async def test_match_md5_with_data():
    """
    Test the match_md5_with_data function.

    Raises:
        AssertionError: If the matched_data pattern, description, or equality assertions fail.
    """
    md5 = "924a68d347c80d0e502157e83812bb23"
    data = {
        "^(?:924a68d347c80d0e502157e83812bb23|f1ac749564d5ba793550ec6bdc472e7c|ef9c0362bf20a086bb7c2e8ea346b9f0)$": {
            "@pattern": "^(?:924a68d347c80d0e502157e83812bb23|f1ac749564d5ba793550ec6bdc472e7c"
                        "|ef9c0362bf20a086bb7c2e8ea346b9f0)$",
            "description": "Roundcube Webmail",
            "example": [
                "924a68d347c80d0e502157e83812bb23",
                "f1ac749564d5ba793550ec6bdc472e7c",
                "ef9c0362bf20a086bb7c2e8ea346b9f0"
            ],
            "param": [
                {
                    "@pos": "0",
                    "@name": "service.vendor",
                    "@value": "Roundcube"
                },
                {
                    "@pos": "0",
                    "@name": "service.product",
                    "@value": "Webmail"
                },
                {
                    "@pos": "0",
                    "@name": "service.cpe23",
                    "@value": "cpe:/a:roundcube:webmail:-"
                }
            ]
        }
    }

    matched_data = await match_md5_with_data(md5, data)
    assert matched_data is not None
    assert (
            matched_data["@pattern"].strip()
            == "^(?:924a68d347c80d0e502157e83812bb23|f1ac749564d5ba793550ec6bdc472e7c|ef9c0362bf20a086bb7c2e8ea346b9f0)$"
    )
    assert matched_data["description"] == "Roundcube Webmail"
