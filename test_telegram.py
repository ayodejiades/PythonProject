import requests
import json
import time

# URL of your local running FastAPI app
URL = "http://127.0.0.1:8000/webhook"

def test_start_command():
    print("Sending /start command...")
    payload = {
        "update_id": 10001,
        "message": {
            "message_id": 1,
            "date": int(time.time()),
            "chat": {
                "id": 123456789,
                "type": "private",
                "username": "Student",
                "first_name": "Naija",
                "last_name": "Boy"
            },
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Naija",
                "last_name": "Boy",
                "username": "Student"
            },
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}]
        }
    }
    
    try:
        response = requests.post(URL, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def test_text_message():
    print("\nSending text message 'How far?'...")
    payload = {
        "update_id": 10002,
        "message": {
            "message_id": 2,
            "date": int(time.time()),
            "chat": {
                "id": 123456789,
                "type": "private"
            },
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Naija"
            },
            "text": "How far?"
        }
    }
    
    try:
        response = requests.post(URL, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    print("Testing Telegram Webhook logic locally...")
    print("ensure 'uvicorn main:app --reload' is running in another terminal.")
    test_start_command()
    test_text_message()
