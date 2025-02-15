import os
import shutil

def delete_migration_files():
    for root, dirs, files in os.walk('./apps'):
        for dir in dirs:
            if dir == 'migrations':
                migration_dir = os.path.join(root, dir)
                for file in os.listdir(migration_dir):
                    file_path = os.path.join(migration_dir, file)
                    if file != '__init__.py':
                        try:
                            os.remove(file_path)
                            print(f'Archivo eliminado: {file_path}')
                        except PermissionError as e:
                            print(f'Error de permiso al eliminar {file_path}: {e}')
                print(f'Archivos de migración eliminados en: {migration_dir}')

def delete_cache_files():
    for root, dirs, files in os.walk('./apps'):
        for dir in dirs:
            if dir == '__pycache__':
                cache_dir = os.path.join(root, dir)
                try:
                    shutil.rmtree(cache_dir)
                    print(f'Archivos de caché eliminados en: {cache_dir}')
                except PermissionError as e:
                    print(f'Error de permiso al eliminar {cache_dir}: {e}')

if __name__ == "__main__":
    delete_migration_files()
    delete_cache_files()