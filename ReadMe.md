# LeetCode Bot

This is a Telegram bot that keeps users accountable by tracking daily submissions. It is also able to provide the daily question.

## Features

- **Start Command**: Sends a welcome message and instructions.
- **Question of the Day**: Fetches and displays the LeetCode Question of the Day.
- **Daily Submissions**: Displays the daily submissions of specified users.
- **Solved Problems**: Displays the number of problems solved by each user.
- **Badges**: Displays the badges earned by each user.

## Setup

### Prerequisites

- Python 3.7+
- Telegram account

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/leetcode-bot.git
   cd leetcode-bot

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt

3. **Configure the Bot**:
   - Use [BotFather](https://core.telegram.org/bots#botfather) on Telegram to create a new bot and get the token.
   - Create a `config.py` file in the root directory and add the following:
     ```python
     TOKEN = 'your-telegram-bot-token'
     BOT_USERNAME = 'your-bot-username'
     USERS = ['user1', 'user2', 'user3']  # List of LeetCode usernames to track
     ```
   - Add commands to your Telegram bot in BotFather:
     ```
     start - Display opening message
     qod - Question of the day
     submissions - Daily submissions
     solved - Number of problems solved by each user
     badges - Display the badges earned by each user
     ```
     Ensure the command names match those in `main.py`

## Running the Bot

### Run the bot:
   ```sh
   python main.py
   ```

### Interact with the bot:
- Use `/Start` to get a welcome message.
- Use `/QOD` to get the LeetCode Question of the Day.
- Use `/Submissions` to get the daily submissions of the specified users.
- Use `/Solved` to get the number of problems solved by each user (categorised by difficulty).
- Use `/Badges` to get the badges earned by each user.

## Error Logging

Errors are logged to the console for debugging purposes.

## Helper Functions

- `fetch_qod()`: Fetches the Question of the Day from an API.
- `format_qod(data)`: Formats the Question of the Day data.
- `parse_html(html)`: Parses HTML content to plain text.
- `get_user_submissions(username)`: Fetches the latest submissions of a user.
- `get_todays_submissions(submissions)`: Filters submissions to get today's submissions.
- `get_solved_problems(user)`: Fetches the number of problems solved by the user.
- `get_badges(user)`: Fetches the name of the badges earned by the user
