import os



class Settings:
    ACCESS_DATABASE_URL = r'C:\NextRevol\nuFa\NufaersatzteileProject\App\db\NuFa.accdb'
    ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'

settings = Settings()