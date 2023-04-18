import requests

# Define the endpoint URL
url = "http://localhost:8080/login"

# Define the form data
data1 = {
    "username": "ed34depto32",
    "password": "123"
}

data2 = {
    "username": "ed34depto32",
    "password": "111"
}

data3 = {
    "username": "ed34depto123",
    "password": "111"
}

# Make the request
response = requests.post(url, data=data1)

# Check the response status code
if response.status_code == 200:
    print(response.text)
else:
    print("Login failed.")


# Make the request
response = requests.post(url, data=data2)

# Check the response status code
if response.status_code == 200:
    print(response.text)
else:
    print("Login failed.")


# Make the request
response = requests.post(url, data=data3)

# Check the response status code
if response.status_code == 200:
    print(response.text)
else:
    print("Login failed.")
