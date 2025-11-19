from dotenv import load_dotenv
load_dotenv()

from src.lib.config.config import Config

settings = Config()

def main():
    print(settings.DATABASE_URL)

if __name__ == '__main__':
    main()