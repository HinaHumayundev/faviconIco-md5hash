# MD5 Matching with IP Addresses

This is a FastAPI application that matches MD5 hash values with IP addresses and retrieves corresponding data. The application uses the provided IP addresses to fetch favicons from the respective websites, calculates the MD5 hash of the favicon content, and matches it with pre-defined data stored in an XML file.

## Requirements

- Python 3.7 or higher
- FastAPI
- pydantic
- aiohttp
- xmltodict
- BeautifulSoup

#### pip install -r requirements.txt

## Usage
1) Place the favicons.xml file containing the pre-defined data in the project's src folder.

2) Start the FastAPI application:
 uvicorn main:app --reload 
3) The application will start running on http://localhost:8000. You can access the API documentation at http://localhost:8000/docs. 
4) To match MD5 hash values with IP addresses, send a POST request to /md5-matching with the following JSON payload:

```
{
  "ip_addresses": [
   "134.209.150.228", 
   "192.168.0.1-192.168.0.10", 
   "185.182.56.42", 
   "134.209.150.228"
  ]
}

````
The ip_addresses field should contain a list of IP addresses and or IP address ranges (with - notation) you want to match.
5) The response will contain the matched data for each IP address:

```
 {
  "matched_data": [
    {
      "@pattern": "924a68d347c80d0e502157e83812bb23",
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
        }
      ]
    }
  ]
}

```

## Testing

To run the tests for this project, follow these steps:

1) Make sure all the project dependencies are installed. You can install them by running:

   ```bash
   pip install -r requirements.txt

2) Start the tests by running the following command:
   pytest
3) #### Note: The tests require an active internet connection to fetch favicons and perform matching. If the tests fail due to connectivity issues, please check your internet connection and try again.

4) The tests include the following:

    - ###### test_md5_matching: Tests the MD5 matching endpoint with various IP addresses and expected matched counts. It verifies the response status code, the presence of "matched_data" in the response JSON, and the length of the matched data.
    - ###### test_match_md5_with_data: Tests the match_md5_with_data function. It verifies the pattern, description, and equality of the matched data.
If all the tests pass, you will see the test results in the console.

#### Note: The tests use the logging.error function to verify the logging of error messages. If a test case includes an invalid IP address, an error message should be logged. Make sure to review the test results and check if the error messages are logged correctly.

5) You can also view the test coverage report by running:
   pytest --cov=main

## Running the Application and Tests using Docker

To run the application and tests using Docker, follow these steps:

1) Make sure you have Docker installed on your system.

2) Build the Docker image by running the following command:

```bash
docker-compose build
```

3) Start the application by running the following command:
   
```bash
docker-compose up -d
```

5) Run the tests by executing the following command:

```bash
docker-compose run app python -m pytest

```
5) Stop the application by running the following command:

```bash
docker-compose down
```

