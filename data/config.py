import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PGUSER = str(os.getenv("POSTGRES_USER"))
PGPASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
DATABASE = str(os.getenv("DB_NAME"))
TGSTAT_TOKEN = str(os.getenv('TGSTAT_TOKEN'))
SHOP_ID = str(os.getenv('SHOP_ID'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))

admins = [
    233153169,
    1955750981
]

ip = os.getenv("ip")

POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"
