import gspread_pandas
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
gspread_pandas.conf.get_config_dir()
