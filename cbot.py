#!/usr/bin/env python3
import os
from openai import OpenAI

client = OpenAI()
import json
import sys
import sqlite3
import pyperclip

def initDB():
    from os.path import expanduser
    home = expanduser("~")
    global cache 
    cache = sqlite3.connect(home + "/.cbot_cache") 
    cache.execute("""
                    CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY,
                    question TEXT,
                    answer TEXT,
                    count INTEGER DEFAULT 1)""")

def closeDB():
    cache.commit()
    cache.close()

def checkQ(question_text):
    answer = cache.execute("SELECT id,answer,count FROM questions WHERE question = ?", (question_text,))
    answer = answer.fetchone()
    if answer:
        response = answer[1]
        newcount = int(answer[2]) + 1
        cache.execute("UPDATE questions SET count = ? WHERE id = ?", (newcount, answer[0]))
        return response
    else:
        return False

def insertQ(question_text, answer_text):
    cache.execute("DELETE FROM questions WHERE question = ?", (question_text,))
    cache.execute("INSERT INTO questions (question,answer) VALUES (?,?)", (question_text, answer_text))

def fetchQ():
    question = " ".join(sys.argv[1:]).strip()
    return question

def parseOptions(question):
    global question_mode
    global execute
    global clip
    global shortcut
    shortcut = ""
    execute = False
    clip = False
    question_mode = "normal"
    if "-h" in question or question == " ":
        print("Cbot is a simple utility powered by GPT models")
        print("""
        Example usage:
        cbot how do I copy files to my home directory
        cbot "How do I put my computer to sleep?"
        cbot -c "how do I install homebrew?"      (copies the result to clipboard)
        cbot -x what is the date                  (executes the result)
        cbot -g who was the 22nd president        (runs in general question mode)
        """)
        exit()

    if "-x" in question:
        execute = True
        question = question.replace("-x ", "")

    if "-c" in question:
        clip = True
        question = question.replace("-c ", "")

    if "-g" in question:
        question_mode = "general"
        question = question.replace("-g ", "")

    if "-s" in question:
        question_mode = "shortcut"
        question = sys.argv[2]
        shortcut = sys.argv[3]

    return question

def main():
    if os.getenv("OPENAI_API_KEY") is None:
        print("Please set your OpenAI API key as an environmental variable")
        print("Learn more at https://platform.openai.com/account/api-keys")
        print("To set the environment variable, run: export OPENAI_API_KEY=your-key")
        exit()

    global question
    question = fetchQ()
    question = parseOptions(question)

    platform = sys.platform
    if platform == "darwin":
        platform = "Mac"
    elif platform == "win32":
        platform = "Windows"
    else:
        platform = "Linux"

    initDB()

    if question_mode == "shortcut":
        insertQ(question, shortcut)
        print("Saving Shortcut")
        cache_answer = False
    else:
        cache_answer = checkQ(question)

    if not cache_answer and question_mode in ["general", "normal"]:
        prompt = f"I am a command line translation tool for {platform}. Ask me a question, and I'll provide a Unix command to achieve it. I will only return the command with no further explanation."
        if question_mode == "general":
            prompt = "I answer general knowledge questions."

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]

        # Adjust for openai.ChatCompletion changes
        response = client.chat.completions.create(model="gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=100)
        result = response.choices[0].message.content.strip()
        insertQ(question, result)
    else:
        result = cache_answer
        if question_mode != "shortcut":
            print("💾 Cache Hit")

    if clip:
        pyperclip.copy(result)
    if execute:
        print(f"cbot executing: {result}")
        if "sudo" in result:
            print("Execution canceled, cbot will not execute sudo commands.")
        else:
            os.system(result)
    else:
        if question_mode != "shortcut":
            print(result)

    closeDB()

if __name__ == "__main__":
    sys.exit(main())
