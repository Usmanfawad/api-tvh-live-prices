import os
# from dotenv import load_dotenv
# from pathlib import Path


class Settings:

    ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
    ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'

settings = Settings()