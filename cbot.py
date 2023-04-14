#!/usr/bin/env python3
from os.path import expanduser
import os
import openai
import json
import sys
import sqlite3
import pyperclip
from dotenv import load_dotenv
import time


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

global question
question = ""


def initDB():
    global cache
    cache = sqlite3.connect(home + "/.cbot_cache")
    cache.execute("""
                   CREATE TABLE IF NOT EXISTS questions 
                   (id INTEGER PRIMARY KEY,
                   question TEXT,
                   answer TEXT,
                   count INTEGER DEFAULT 1,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

    cache.execute("""
                   CREATE TABLE IF NOT EXISTS conversations 
                   (id INTEGER PRIMARY KEY,
                   messages TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")


def closeDB():
    cache.commit()
    cache.close()


def checkQ(question_text):
    answer = cache.execute(
        "SELECT id,answer,count FROM questions WHERE question = ?", (question_text,))
    answer = answer.fetchone()
    if (answer):
        response = answer[1]
        newcount = int(answer[2]) + 1
        counter = cache.execute(
            " UPDATE questions SET count = ? WHERE id = ?", (newcount, answer[0]))
        return(response)
    else:
        return(False)


def store_messages(messages):
    messages_json = json.dumps(messages)
    timestamp = int(time.time())
    cache.execute(
        "INSERT INTO conversations (messages, timestamp) VALUES (?, ?)", (
            messages_json, timestamp)
    )
    cache.commit()


def insertQ(question_text, answer_text):
    # Delete the question if it already exists in the database
    cache.execute("DELETE FROM questions WHERE question = ?", (question_text,))
    cache.execute("INSERT INTO questions (question,answer) VALUES (?,?)",
                  (question_text, answer_text))

    # Get the previous message history
    previous_prompts = fetch_previous_prompts()

    # Add the user's message and the assistant's response to the message history
    previous_prompts.append({"role": "user", "content": question_text})
    previous_prompts.append({"role": "assistant", "content": answer_text})

    # Insert the updated message history into the conversations table
    cache.execute("INSERT INTO conversations (messages) VALUES (?)",
                  (json.dumps(previous_prompts[-20:]),))

# def insertQ(question_text, answer_text):
#     answer = cache.execute(
#         "DELETE FROM questions WHERE question = ?", (question_text,))
#     answer = cache.execute(
#         "INSERT INTO questions (question,answer) VALUES (?,?)", (question_text, answer_text))

#     messages = [{"role": "user", "content": question_text},
#                 {"role": "assistant", "content": answer_text}]
#     store_messages(messages)


def fetchQ():
    question = ""
    for a in range(1, len(sys.argv)):
        question = question + " " + sys.argv[a]
    question = question.strip()
    return question


def parseOptions(question):
    global question_mode
    global general_q
    global execute
    global clip
    global shortcut
    shortcut = ""
    execute = False
    clip = False
    question_mode = "normal"
    if ("-h" in question) or (question == " "):
        print("Cbot is a simple utility powered by GPT3")
        print("""
        Example usage:
        cbot how do I copy files to my home directory
        cbot "How do I put my computer to sleep
        cbot -c "how do I install homebrew?"      (copies the result to clipboard)
        cbot -x what is the date                  (executes the result)
        cbot -g who was the 22nd president        (runs in general question mode)
        """)
        exit()

    if ("-x" in question):
        execute = True
        question = question.replace("-x ", "")

    if ("-c" in question):
        clip = True
        question = question.replace("-c ", "")

    if ("-g" in question):
        question_mode = "general"
        question = question.replace("-g ", "")

    if ("-s" in question):
        question_mode = "shortcut"
        question = sys.argv[2]
        shortcut = sys.argv[3]

    return(question)


def fetch_previous_prompts():
    prompts = cache.execute(
        "SELECT messages FROM conversations ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()
    previous_prompts = []

    for prompt in prompts:
        messages = json.loads(prompt[0])
        previous_prompts.extend(messages)

    return previous_prompts


platform = sys.platform
if platform == "darwin":
    platform = "Mac"
elif platform == "win32":
    platform = "Windows"
else:
    platform = "Linux"

question = fetchQ()
question = parseOptions(question)

home = expanduser("~")
initDB()

if (question_mode == "shortcut"):
    insertQ(question, shortcut)
    print("Saving Shortcut")
    cache_answer = False
else:
    cache_answer = checkQ(question)

response = ""
if not(cache_answer) and ((question_mode == "general") or (question_mode == "normal")):
    temp_question = question
    if not("?" in question):
        temp_question = question + "?"

    if (question_mode == "general"):
        system_message = "You are a helpful assistant. Answer the user's question in the best way possible."
    else:
        system_message = f"You are a command line translation tool for {platform}. You will answer the user's question with the correct unix command."

    previous_prompts = fetch_previous_prompts()

    prompt = [{"role": "system", "content": system_message}] + previous_prompts

    prompt += [{"role": "user", "content": temp_question}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = response.choices[0].message["content"]
    insertQ(question, result)

else:
    result = cache_answer
    if not(question_mode == "shortcut"):
        print("💾 Cache Hit")

if clip:
    pyperclip.copy(result)
if execute:
    print("cbot executing: " + result)
    if ("sudo" in result):
        print("Execution canceled, cbot will not execute sudo commands.")
    else:
        result = os.system(result)
else:
    if not(question_mode == "shortcut"):
        print(result)

closeDB()
