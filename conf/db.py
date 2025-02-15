import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PostgreSQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gesinv',
        'USER': 'gesinv_user',
        'PASSWORD': 'fqDn0rpkOZipXEqDtbAOKJVFUBLjbaQ9',
        'HOST': 'dpg-cuks022n91rc73auns5g-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

SQLite3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gesinv.sqlite3',
    }
}

GetEnv = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}