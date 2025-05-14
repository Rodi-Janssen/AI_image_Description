import watch_directory
from pathlib import Path

# Folder to watch
folder_to_process = Path(__file__).parent / "images"

if __name__ == "__main__":
    watch_directory.watch_directory(folder_to_process)
