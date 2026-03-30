import traceback
import sys

with open('error_log.txt', 'w', encoding='utf-8') as f:
    try:
        from transformers import pipeline
        print("Imported pipeline.")
        p = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        f.write("Success!\n")
    except Exception as e:
        f.write("Error occurred:\n")
        traceback.print_exc(file=f)
