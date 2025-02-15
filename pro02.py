import os

def manage_django():
    os.system('python manage.py makemigrations')

    os.system('python manage.py migrate')
    
    os.system('python manage.py runserver')

if __name__ == "__main__":
    manage_django()