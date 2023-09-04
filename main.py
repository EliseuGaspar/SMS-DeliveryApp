from src.views.classes.app import Delivery
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    Delivery().run()