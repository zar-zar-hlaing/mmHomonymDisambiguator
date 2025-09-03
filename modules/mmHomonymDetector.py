# homonym_detector.py
import os
from typing import List

import sys, os
# add current folder (modules/) to path
sys.path.append(os.path.dirname(__file__))
from mmTokenizer import syllableSegment

# Current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up to project root
base_dir = os.path.abspath(os.path.join(current_dir, ".."))

# Correct path to homonym file
HOMONYM_FILE_PATH = os.path.join(base_dir, "myanmar_text_data", "HomonymWords.txt")

def detect_homonyms(tokenized_text: str) -> List[str]:
    try:
        with open(HOMONYM_FILE_PATH, "r", encoding="utf-8") as f:
            homonym_sets = [set(line.strip().split()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Homonym file not found at {HOMONYM_FILE_PATH}")
        return []
    except Exception as e:
        print(f"Error reading file {HOMONYM_FILE_PATH}: {e}")
        return []

    tokens = [t.strip() for t in tokenized_text.split("|") if t.strip()]
    detected_homonym_lst = [t for t in tokens if any(t in s for s in homonym_sets)]
    return detected_homonym_lst


if __name__ == "__main__":
    # Example tokenized input string
    # tokenized_test_input = "ကျောင်း,သား,များ,စာ,ကြိုး,စား,နေ,ကြ,သည်,။"
    test_input = "ကျောင်းသားများစာကြိုးစားနေကြသည်။"
    tokenized_test_input = syllableSegment(test_input)
    
    # Detect homonyms
    results = detect_homonyms(tokenized_test_input)
    
    print("___Detected homonyms:___", results)
