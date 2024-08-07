from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

import os
from typing import Final

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
USERS = os.getenv("USERS").split(",")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Reminder to practice LeetCode daily. Use /QOD to get the Question of the Day and /Submissions to get the daily submissions.")

async def question_of_the_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = fetch_qod()
    formatted_data = format_qod(data)
    await update.message.reply_text(formatted_data, disable_web_page_preview=True, parse_mode='Markdown')

async def daily_submissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    combined_text = ""
    for user in USERS:
        submissions = get_user_submissions(user)
        todays_submissions = get_todays_submissions(submissions)
        if todays_submissions:
            combined_text += f"User: {user}\n"
            for subs in todays_submissions:
                combined_text += f"Title: [{subs['title']}]({subs['url']})\nCompleted on: {subs['timestamp']}\n\n"
        else:
            combined_text += f"User: {user}\nNo submissions for today.\n\n"

    await update.message.reply_text(combined_text if combined_text else "No submissions for today.", disable_web_page_preview=True, parse_mode='Markdown')


async def solved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in USERS:
        solved_problems = get_solved_problems(user)
        solved_problems_text = f"User: {user}\n"
        for key, value in solved_problems.items():
            solved_problems_text += f"{key}: {value}\n"
        await update.message.reply_text(solved_problems_text, disable_web_page_preview=True)


# Error Logging
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Helper Functions
def fetch_qod():
    url = "https://alfa-leetcode-api.onrender.com/daily"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")

def format_qod(data):
    title = data.get("questionTitle", "N/A")
    difficulty = data.get("difficulty", "N/A")
    question = parse_html(data.get("question", "N/A"))
    url = data.get("questionLink", "N/A")

    formatted_string = (f"Title:   [{title}]({url})\n"
                        f"Difficulty:   {difficulty}\n\n"
                        f"Question:\n{question}\n")
    return formatted_string

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def get_user_submissions(username):
    url = f"https://alfa-leetcode-api.onrender.com/{username}/acSubmission?limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("submission", [])
    else:
        print(f"Failed to fetch data: {response.status_code}")

def get_todays_submissions(submissions):
    sg_timezone = pytz.timezone("Asia/Singapore")
    today = datetime.now(sg_timezone).date()
    base_url = "https://leetcode.com/problems/"
    todays_submissions = [
        {
            'title': sub.get('title'),
            'url': f"{base_url}{sub.get('titleSlug')}/",
            'timestamp': datetime.fromtimestamp(int(sub['timestamp']), sg_timezone).strftime('%Y-%m-%d %H:%M:%S')
        }
        for sub in submissions
        if datetime.fromtimestamp(int(sub['timestamp']), sg_timezone).date() == today
    ]
    return todays_submissions

def get_solved_problems(username):
    url = f"https://alfa-leetcode-api.onrender.com/{username}/solved"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        renamed_data = {
            "Total Solved": data.get("solvedProblem", 0),
            "Easy": data.get("easySolved", 0),
            "Medium": data.get("mediumSolved", 0),
            "Hard": data.get("hardSolved", 0),
        }
        return renamed_data.get("solved", [])
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Main
if __name__ == "__main__":
    print('Starting Bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("Start", start_command))
    app.add_handler(CommandHandler("QOD", question_of_the_day))
    app.add_handler(CommandHandler("Submissions", daily_submissions))
    app.add_handler(CommandHandler("Solved", solved))

    # Error Logging
    app.add_error_handler(error)

    # Polling
    print('Bot is running...')
    app.run_polling(poll_interval=2)




