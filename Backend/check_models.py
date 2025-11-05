import google.generativeai as genai

# 🗝️ Replace with your actual API key
genai.configure(api_key="AIzaSyDQ8i-bdiOWxNXc1Cn5MlMI94eh6zXiaY0")

print("✅ Connected successfully! Available models:")
for model in genai.list_models():
    print(" -", model.name)
