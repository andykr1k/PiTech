import os

def upload_manifest(file_name):
    path = f'./Data/manifests/{file_name}'
    if not os.path.exists(path):
        print(f"Manifest '{file_name}' not found.")
        return None
    with open(path, 'r') as manifest_file:
        return manifest_file.readlines()


def upload_transfer_list(file_name):
    path = f'./Data/transferlist/{file_name}'
    if not os.path.exists(path):
        print(f"Transfer List '{file_name}' not found.")
        return None
    with open(path, 'r') as transfer_list:
        return transfer_list.readlines()
