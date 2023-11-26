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
        modified_data = []

        for entry in data:
            if 'body' in entry and entry['body']:
                headings = extract_headers(entry['body'])
                entry['context'] = headings
                modified_data.append(entry)

        with open(output_file, 'w') as outfile:
            json.dump(modified_data, outfile, indent=2)
    except Exception as e:
        print('Error', e)


# Example usage:
input_json_file = './UITS-data.json'
output_json_file = './UITS-output.json'

modify_json(input_json_file, output_json_file)
