import json
import os


def read_txt_files(folder_path):
    json_objects = []

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Extract URL from the first line
            url = lines[0].strip()

            # Combine the rest of the lines to form the body
            body = ' '.join(line.strip() for line in lines[1:])

            # Create JSON object
            json_object = {
                "url": url,
                "body": body
            }

            # Add JSON object to the list
            json_objects.append(json_object)

    return json_objects


def write_to_json_file(json_objects, output_file):
    # Write the JSON array to a file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_objects, json_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Specify the folder containing the .txt files
    folder_path = "./scraped/"

    # Specify the output JSON file
    output_file = "data3.json"

    # Read .txt files and create JSON objects
    json_objects = read_txt_files(folder_path)

    # Write JSON objects to a .json file
    write_to_json_file(json_objects, output_file)

    print(f"Conversion complete. JSON objects written to {output_file}")
