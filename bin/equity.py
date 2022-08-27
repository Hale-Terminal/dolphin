import requests


test_e = {
    "ticker": "TESTF",
    "name": "Test Equity",
    "description": "Test Description",
    "street1": "street1",
    "street2": "street2",
    "city": "Waterford",
    "state": "MI",
    "zip": "00000",
    "country_code": "US",
    "exchange": "exchange",
    "ein": "1020338301",
    "phone": "000-000-0000",
    "cik": 100103923,
    "state_of_incorporation": "MI",
    "website": "website",
    "sector": "sector",
    "industry": "industry",
}

test_u = {
    "ticker": "UPDATETESTF",
    "name": "Test Equity",
    "description": "Test Description",
    "street1": "street1",
    "street2": "street2",
    "city": "Waterford",
    "state": "MI",
    "zip": "00000",
    "country_code": "US",
    "exchange": "exchange",
    "ein": "1020338301",
    "phone": "000-000-0000",
    "cik": 100103923,
    "state_of_incorporation": "MI",
    "website": "website",
    "sector": "sector",
    "industry": "industry",
}

headers = {"accept": "application/json", "Content-Type": "application/json"}

login_data = {"username": "AHALE", "password": "drewhale"}

u1 = requests.post("http://127.0.0.1:8000/api/v1/auth/login", headers=headers, json=login_data)
if u1.status_code == 200:
    login_response = u1.json()
    token = "bearer " + login_response["token"]
    headers["Authorization"] = token
else:
    print(u1.status_code)


# u2 = requests.get("http://127.0.0.1:8000/api/v1/equity/ticker/AAPL", headers=headers)
# print(u2.json())

# u3 = requests.post("http://127.0.0.1:8000/api/v1/equity", headers=headers, json=test_e)
# if u3.status_code != 200:
#    print(u3.content)
#    exit(0)

# u4 = requests.put("http://127.0.0.1:8000/api/v1/equity/101", headers=headers, json=test_u)
# print(u4.json())

# u5 = requests.delete("http://127.0.0.1:8000/api/v1/equity/102", headers=headers)
# print(u5.status_code)


u6 = requests.get("http://127.0.0.1:8000/api/v1/search", headers=headers)
print(u6.json())
