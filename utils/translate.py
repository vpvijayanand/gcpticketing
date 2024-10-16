from google.cloud import translate_v2 as translate

# Initialize Google Cloud Translation client
translate_client = translate.Client()

# Function to detect language and translate to English if necessary
def detect_and_translate_text(text):
    # Detect the language of the text
    result = translate_client.detect_language(text)
    detected_language = result['language']

    # If the detected language is not English, translate the text
    if detected_language != 'en':
        translation = translate_client.translate(text, target_language='en')
        translated_text = translation['translatedText']
        return translated_text, detected_language
    else:
        return text, 'en'  # No translation needed, return the original text
