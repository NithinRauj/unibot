import os
import json
import re


def extract_headers(paragraph):
    # Regular expression to match headings annotated with #, ##, ###, ####
    try:
        headers = []
        pattern = re.compile(
            r'(#{1,4})\s+([^\n]+?)(?=\s{2}|$)', re.MULTILINE)
        matches = pattern.findall(paragraph)
        for match in matches:
            headers.append(match[1])
        return headers
    except Exception as e:
        print('Error in extracting headers', e)
        return []


def modify_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        infile.close()
        modified_data = []

        for entry in data:
            if 'body' in entry and entry['body']:
                headings = extract_headers(entry['body'])
                entry['context'] = headings
                modified_data.append(entry)

        with open(output_file, 'a', encoding='utf-8') as outfile:
            json.dump(modified_data, outfile, indent=2, ensure_ascii=False)
        outfile.close()
    except Exception as e:
        print('Error', e)


if __name__ == '__main__':
    input_folder_path = 'data'
    output_folder_path = 'processed_data'
    output_file = 'data.json'
    output_file_path = os.path.join(output_folder_path, output_file)

    for filename in os.listdir(input_folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder_path, filename)
            print(file_path)
            modify_json(file_path, output_file_path)
