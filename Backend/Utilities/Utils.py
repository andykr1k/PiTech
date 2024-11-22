import os
import re

def upload_manifest(file_name):
    path = os.path.join('Data', 'manifests', file_name)

    if not os.path.exists(path):
        print(f"Manifest '{file_name}' not found in path: {path}")
        return None
    with open(path, 'r') as manifest_file:
        manifestData = []
        for line in manifest_file:
            parsedLine = re.findall(r'\[[^\]]+\]|\{[^\}]+\}|\w+(?: \w+)*', line)
            for item in parsedLine:
                manifestData.append(item)
        return manifestData


def upload_transfer_list(file_name):
    path = os.path.join('Data', 'transferlist', file_name)

    if not os.path.exists(path):
        print(f"Transfer List '{file_name}' not found.")
        return None
    with open(path, 'r') as transfer_list:
        return transfer_list.readlines()
