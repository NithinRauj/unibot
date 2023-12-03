import json


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Replace 'your_file.json' with the actual path to your JSON file
file_path = './processed_data/data.json'
json_data = read_json_file(file_path)

if json_data:
    print("JSON data read successfully:")
    print(json_data)
