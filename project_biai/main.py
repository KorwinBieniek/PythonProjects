# Tylko klasy 0, 1, 2, 5, 7, 10

import os


def read_text_file(file_path):
    with open('output/' + file_path, 'w') as write_file:
        with open(file_path, 'r') as read_file:
            print(f'\n{file_path}\n')
            while True:
                content = read_file.readline()
                if not content:
                    break
                if content.startswith(('0', '1', '2', '5', '7', '10')):
                    if content.startswith('5'):
                        content = content.replace('5', '3')
                    elif content.startswith('7'):
                        content = content.replace('7', '4')
                    elif content.startswith('10'):
                        content = content.replace('10', '5')
                    write_file.write(content)

os.chdir('input/')
for file in os.listdir():
    if file.endswith('.txt'):
        file_path = f"{file}"
        read_text_file(file_path)