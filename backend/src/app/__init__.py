from pathlib import Path

BASE_DIECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = BASE_DIECTORY.joinpath("data")

print("DATA_DIRECTORY", BASE_DIECTORY)
