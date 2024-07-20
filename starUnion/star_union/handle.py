import subprocess
import os
from pathlib import Path
import shutil
import sys


base_path = Path(__file__).resolve().parent.parent / 'star_union'
base_path = str(base_path).replace('\\', '\\\\')

wanted_to_move_from_main = [
    'Male.png',
    'Female.png',
    'Baby_Male.png',
    'Baby_Female.png',
    'Profile Avatar.png'
]
# Define the list of management commands to run

def handle_photos_files():
    root = base_path + '/main/User_profile_images'
    if os.path.exists(root) :
        for file in os.listdir(root):
            if file in wanted_to_move_from_main:
                shutil.move(root + '/' + file, base_path + '/star_union/assets' )
        shutil.rmtree(root, ignore_errors=True)


def migrations():
    commands = [
        'python manage.py makemigrations',
        'python manage.py migrate --database=main_db',

        # Add more commands as needed
    ]

    # Iterate over the list of commands and execute each one
    for command in commands:
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

    os.environ['DJANGO_SUPERUSER_PASSWORD'] = '0123456789Ss'
    command = [
        'python', 'manage.py', 'createsuperuser',
        '--username', 'test',
        '--email', 'test@test.com',
        '--noinput',
        '--database=main_db',  # Prevents prompts for input

    ]
    subprocess.run(command, text=True)

    command = [
        'python',
        'manage.py',
        'runserver'
    ]
    subprocess.run(command, text=True)


def deleteMigrations(directory):
    items = os.listdir(directory)
    folders = [item for item in items if os.path.isdir(
        os.path.join(directory, item))]
    tes = directory.split('\\')
    if tes[len(tes) - 1] == 'star_union':
        files = [item for item in items if os.path.isfile(
            os.path.join(directory, item))]
        for file in files:
            if file.endswith('.sqlite3'):
                os.remove(directory + "\\" + file)
    if tes[len(tes) - 1] == 'migrations' and tes[len(tes) - 2] != 'db':
        files = [item for item in items if os.path.isfile(
            os.path.join(directory, item))]
        for file in files:
            if file != '__init__.py':
                os.remove(directory + "\\" + file)
    for folder in folders:
        if folder == '__pycache__':
            shutil.rmtree(directory + "\\" + folder, ignore_errors=True)
        else:
            deleteMigrations(directory + "\\" + folder)



if (len(sys.argv) > 1):
    if sys.argv[1].lower() == 'production' :
        handle_photos_files()
        deleteMigrations(base_path)
else :
    deleteMigrations(base_path)
    # # put your django env path
    deleteMigrations('C:\\Users\\aba\\Downloads\\env\\Lib\\site-packages\\django')
    migrations()

