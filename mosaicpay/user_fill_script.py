import time
import requests
from requests.exceptions import ConnectionError

data = [
		{
			"first_name": "John",
			"last_name": "Doe",
			"birthday": "1990-01-01",
			"email": "johndoe@example.com",
			"password": "password123"
		},
	
		{
			"first_name": "Jane",
			"last_name": "Smith",
			"birthday": "1985-05-10",
			"email": "janesmith@example.com",
			"password": "qwerty456"
		},

		{
			"first_name": "Michael",
			"last_name": "Johnson",
			"birthday": "1995-09-15",
			"email": "michael@example.com",
			"password": "abcdef123"
		},
	
		{
			"first_name": "Emily",
			"last_name": "Davis",
			"birthday": "1992-07-20",
			"email": "emily@example.com",
			"password": "p@ssw0rd"
		},
	
	
		{
			"first_name": "David",
			"last_name": "Wilson",
			"birthday": "1988-03-05",
			"email": "david@example.com",
			"password": "secret123"
		}
]

max_retries = 10
retry_delay = 5

# Wait for the Django server to start
time.sleep(20)

# Make API requests to create users with retries
for user_data in data:
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post('http://localhost:8000/user/', json=user_data)
            if response.status_code == 201:
                print(f"User with email {user_data['email']} created successfully.")
            else:
                print(f"Failed to create user with email {user_data['fields']['email']}.")
            break
        except ConnectionError:
            print(f"Connection refused. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"Max retries exceeded. Failed to create user with email {user_data['fields']['email']}.")

print("User creation script executed successfully.")
