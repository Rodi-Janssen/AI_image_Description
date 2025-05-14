import ollama
import shutil
import os

# Prompt for image analysis
prompt = '''Describe this image in as much detail as possible. Include information about objects, people, background, colors, emotions, context, and anything that might not be obvious at first glance.'''

# Image extensions to process
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')

def is_supported_image(file_path):
    return file_path.lower().endswith(image_extensions)

def on_file_added(file_path):
    print(f"[ADDED] {file_path}")
    proces_file(file_path)

def on_file_moved(src_path, dest_path):
    print(f"[MOVED] {src_path} → {dest_path}")
    # also move txt file.
    if is_supported_image(dest_path):
        move_txt_file(src_path, dest_path)

def move_txt_file(src_path_image, dest_path_image):
    #get txt file paths
    src_path = get_txt(src_path_image)
    dest_path = get_txt(dest_path_image)

    #move txt if found and create it if not found
    if os.path.exists(src_path):
        print(f"moveing txt file {src_path}")
        shutil.move(src_path, dest_path)
    elif not os.path.exists(dest_path):
        proces_file(dest_path_image)

def on_file_delete(path):
    if not is_supported_image(path):
        print(f"Skipped unsupported file: {path}")
        return
    try:
        path_txt = get_txt(path)

        if os.path.exists(path_txt):
            os.remove(path_txt)
            print(f"Deleted: {path_txt}")
        else:
            print(f"No .txt file found at: {path_txt}")
    except ValueError as e:
        print(f"Skipped: {e}")


def get_txt(path):
    base, ext = os.path.splitext(path)
    if ext.lower() in image_extensions:
        return base + ".txt"
    else:
        print("unsupportd image")
        return ""

def proces_file(file_path):
    if not is_supported_image(file_path):
        print(f"Skipped unsupported file: {file_path}")
        return
    process_image(file_path)

def process_image(image_path):
    print(f'Analyzing: {image_path}')
    try:
        response = ollama.chat(
            model='llava',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }]
        )
        #get discription
        description = response['message']['content']
        create_txt_file(description,image_path)
    except Exception as e:
        print(f"Error analyzing {image_path}: {e}")

def create_txt_file(file_content, image_path):
    txt_path = os.path.splitext(image_path)[0] + '.txt'
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(file_content)
    print(f'Saved file at: {txt_path}')
