import dotenv

def load_dotenv_globals() -> str:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    return dotenv_file