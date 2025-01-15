def read_message_body(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_recipients(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()
