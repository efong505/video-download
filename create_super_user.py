import requests
import json

# Create the first super user
AUTH_API = 'https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth'

super_user_data = {
    "email": "super@admin.com",
    "password": "SuperSecure123!",
    "role": "super_user"
}

try:
    response = requests.post(f"{AUTH_API}?action=register", 
                           json=super_user_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 201:
        print("Super User created successfully!")
        print(f"Email: {super_user_data['email']}")
        print(f"Password: {super_user_data['password']}")
        print("Please change this password after first login")
    else:
        print(f"Failed to create Super User: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")