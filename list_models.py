import google.generativeai as genai
import os

# Ensure your environment variable is set before running the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\91888\Desktop\trip planner\google_creds.json"

genai.configure()

models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
