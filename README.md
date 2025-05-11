# Neural Commenting Bot

## Description

This Telegram bot automatically views and comments on stories in groups and channels where you're a member. It uses OpenAI's GPT-3.5 Turbo to generate positive comments in Russian.

## Features

- Automatically detects and processes available stories in your Telegram groups/channels
- Generates context-aware positive comments using AI
- Respects rate limits with built-in anti-flood delays
- Runs continuously with hourly processing cycles
- Handles various error cases gracefully

## Requirements

- Python 3.8+
- Telegram API ID and Hash
- OpenAI API key
- Telethon library
- OpenAI Python client

## Installation

1. Clone this repository or download the script
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Obtain your Telegram API credentials from [my.telegram.org](https://my.telegram.org)
2. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com)
3. Replace `"ВАШ_OPENAI_API_KEY"` in the script with your actual OpenAI key

## Usage

Run the script:
```bash
python neural_commenting.py
```

The script will:
1. Prompt you for your Telegram API ID and Hash
2. Start processing stories in all your groups/channels
3. Run continuously with 1-hour intervals between processing cycles

## Behavior

- Views all available stories in your groups/channels
- Generates positive comments for stories that allow comments
- Leaves one comment every 15 seconds (adjustable)
- Skips stories where comments aren't allowed
- Respects admin permissions and handles errors gracefully

## Customization

You can modify:
- The comment generation prompt in `generate_comment()`
- The delay between comments (currently 15 seconds)
- The processing interval (currently 1 hour)
- The AI model (currently GPT-3.5 Turbo)

## Limitations

- Requires admin rights in groups/channels to function properly
- Currently generates comments only in Russian
- Depends on OpenAI API availability

## Disclaimer

Use this bot responsibly and in compliance with Telegram's Terms of Service. Excessive automated commenting may violate platform rules.
