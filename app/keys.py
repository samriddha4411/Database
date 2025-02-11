import random
import hashlib
import json

def generate_server_key():
    # Generate a random number with 100 digits
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(100)])
    
    # Create a SHA-512 hash of the random number
    server_key = hashlib.sha512(random_number.encode()).hexdigest()
    
    return server_key

def double_sha256(server_key: str, auth_info: dict):
    # Convert the authentication information to JSON format
    auth_info_json = json.dumps(auth_info)
    
    # Concatenate the server key and authentication information
    combined_info = server_key + auth_info_json
    
    # Create the first SHA-256 hash
    first_hash = hashlib.sha256(combined_info.encode()).hexdigest()
    
    # Create the second SHA-256 hash of the first hash
    second_hash = hashlib.sha256(first_hash.encode()).hexdigest()
    
    return second_hash

# Example usage
if __name__ == "__main__":
    server_key = generate_server_key()
    print(f"Generated Server Key: {server_key}")
    
    auth_info = {
        "username": "example_user",
        "password": "example_password"
    }
    hashed_info = double_sha256(server_key, auth_info)
    print(f"Double SHA-256 Hashed Info: {hashed_info}")