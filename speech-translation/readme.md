# Speech Translation with Azure AI

This application demonstrates how to use Azure AI Speech Translation to translate spoken language in real-time. Users can speak phrases in English and have them translated to Spanish, French, or Hindi, with both text output and synthesized speech in the target language.

## Prerequisites

- Python 3.x installed on your system
- An Azure account with an Azure AI Speech resource
- A microphone connected to your computer

## Setup Instructions

1. Clone this repository or download the source code

2. Create a `.env` file in the project root with your Azure AI Speech credentials:
   ```
   SPEECH_KEY=your_speech_key_here
   SPEECH_REGION=your_speech_region_here
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the translator script:
   ```bash
   python translator.py
   ```

2. When prompted, enter the target language code:
   - `fr` for French
   - `es` for Spanish
   - `hi` for Hindi
   - Enter anything else to quit

3. After selecting a language, speak your phrase in English
   - The application will:
     - Transcribe your speech
     - Display the English text
     - Show the translation
     - Play the translated audio in the target language

## Features

- Real-time speech recognition
- Translation to multiple languages (French, Spanish, Hindi)
- Text-to-speech output in the target language
- Support for custom voice selection per language