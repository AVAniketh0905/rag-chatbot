import re


def clean_text(text):
    # Replace repeating characters (e.g., 'DD' -> 'D')
    cleaned_text = re.sub(r"(.)\1", r"\1", text)
    return cleaned_text


# Example: Load the text from a file and clean it
with open("outputs/contents/iibfdigitalbanking.txt", "r", encoding="utf-8") as file:
    original_text = file.read()

cleaned_text = clean_text(original_text)

# Save the cleaned text to a new file
with open("outputs/contents/iibfdigitalbanking.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Cleaned text saved to 'iibfdigitalbanking.txt'.")
