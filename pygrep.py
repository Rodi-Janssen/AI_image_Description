import re
import sys
from pathlib import Path

def grep_txt_files(pattern):
    regex = re.compile(pattern, re.IGNORECASE)
    current_dir = Path(".")
    txt_files = current_dir.rglob("*.txt")

    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for lineno, line in enumerate(f, start=1):
                    match = regex.search(line)
                    if match:
                        col = match.start() + 1  # 1-based column number
                        print(f"{file_path.resolve()}:{lineno}:{col}")
        except Exception as e:
            print(f"Could not read {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pygrep_simple.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    grep_txt_files(pattern)
