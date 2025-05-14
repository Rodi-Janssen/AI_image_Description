from collections import deque
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent
from watchdog.observers import Observer
import ollama_images2
import os
import time

# list of recent deleted files
recent_deletes = deque(maxlen=20)

class SmartEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        created_file(event)

    def on_deleted(self, event):
        if not event.is_directory:
            add_to_deleted_files(event)
            ollama_images2.on_file_delete(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            ollama_images2.on_file_moved(event.src_path, event.dest_path)

def add_to_deleted_files(event):
    filename = os.path.basename(event.src_path)
    recent_deletes.append((filename, event.src_path))

def created_file(event):
    if check_for_move(event):
        return
    ollama_images2.on_file_added(event.src_path)

def check_for_move(event):
    new_file_name = os.path.basename(event.src_path)

    for deleted in list(recent_deletes):
        old_file_name, old_path = deleted
        if new_file_name == old_file_name:
            recent_deletes.remove(deleted)
            ollama_images2.on_file_moved(old_path, event.src_path)
            return True
    return False

def watch_directory(path_to_watch):
    #make observer object to scan directory
    event_handler = SmartEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()
    print(f"Watching directory: {path_to_watch}")

    # use observer to keep scanning untill stoped by ctrl-c
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

