#!/usr/bin/env python3
import os
import openai
import json
import sys    
import sqlite3 
import pyperclip

openai.api_key = os.getenv("OPENAI_API_KEY")
# The recommended approach is to set the API_Key in an environmental
# variable. If you don't want to set that up, you can uncomment this
# line and add your key directly. 
# openai.api_key = "st-key-goes-here"

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
                   count INTEGER DEFAULT 1)""")
def closeDB():
    cache.commit()
    cache.close()

def checkQ(question_text):
    sql = "SELECT id,answer,count FROM questions WHERE question =" + question_text
    answer = cache.execute("SELECT id,answer,count FROM questions WHERE question = ?", (question_text,))
    answer = answer.fetchone()
    if (answer):
        response = answer[1]
        newcount = int(answer[2]) + 1
        counter = cache.execute(" UPDATE questions SET count = ? WHERE id = ?", (newcount,answer[0]))
        return(response)
    else:
        return(False)

def insertQ(question_text,answer_text):
    answer = cache.execute("DELETE FROM questions WHERE question = ?",(question_text,))
    answer = cache.execute("INSERT INTO questions (question,answer) VALUES (?,?)", (question_text,answer_text))

def fetchQ():
    question = ""
    # [cbot,-x,  What,is,the,date]  # execute the response
    # [cbot,What,is, the,date]      # no quotes will work
    # [cbot,What is the date]       # with quotes will work
    for a in range(1,len(sys.argv)):
        question = question + " " + sys.argv[a]
    question = question.strip()
    return question

def parseOptions(question):
    global question_mode    # modes are normal, shortcut and general
    global general_q
    global execute
    global clip
    global shortcut
    shortcut = ""
    execute = False
    clip = False
    question_mode = "normal"
    if ("-h" in question) or (question == " "):  # Return basic help info    
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

    if ("-x" in question):      # Execute the command
        execute = True
        question = question.replace("-x ","") 

    if ("-c" in question):      # Copy the command to clipboard
        clip = True
        question = question.replace("-c ","") 

    if ("-g" in question):      # General question, not command prompt specific 
        question_mode = "general"
        question = question.replace("-g ","") 

    if ("-s" in question):         # Save the command as a shortcut  
        question_mode = "shortcut"
        question=sys.argv[2]
        shortcut = sys.argv[3]

    return(question)


# Detect the platform. This helps with platform specific paths
# and system specific options for certain commands
platform = sys.platform
if platform == "darwin":
    platform = "Mac"
elif platform == "win32":
    platform = "Windows"
else:
    platform = "Linux"

question = fetchQ()
question = parseOptions(question)

# If we change our training/prompts, just delete the cache and it'll 
# be recreated on future runs. 
from os.path import expanduser
home = expanduser("~")
initDB()

#check if we're saving a shortcut
#then check if there's an aswer in our cache
#then execute a GPT3 request as needed

if (question_mode == "shortcut"):
    insertQ(question,shortcut)
    print("Saving Shortcut")
    cache_answer = False 
else:
    cache_answer = checkQ(question)   

if not(cache_answer) and ((question_mode == "general") or (question_mode == "normal")):
    prompt="I am a command line translation tool for "+ platform +"."
    prompt = prompt + """
Ask me what you want to do and I will tell you how to do it in a unix command.
Q: How do I copy a file
cp filename.txt destination_filename.txt
Q: How do I duplicate a folder?
cp -a source_folder/ destination_folder/
Q: How do display a calendar?
cal
Q: how do I convert a .heic file to jpg?
convert source.heic destination.jpg
Q: navigate to my desktop
cd ~/Desktop/
Q: How do I shutdown the computer?
sudo shutdown -h now
"""
    if (question_mode == "general"):     #Alternate prompt for general Q's 
        prompt="Q: Who is Batman?\nBatman is a fictional comic book character.\nQ: What is torsalplexity?\nUnknown\nQ: What is Devz9?\nUnknown\nQ: What is the capital of California?\nSacramento.\nQ: How do you add a comment to a shell script?\nTo add a comment make sure the line starts with a #\nQ: How do I go to the first line using vim\nThe command gg or :1 will go to the first line\nQ: What is Kozar-09?\nUnknown\nQ: What keyboard shortcut cycles tabs in chrome?\nControl+Tab will cycle to the next tab and Shift+Control+Tab will cycle to the previous tab\n"
    temp_question = question
    if not("?" in question):
        temp_question = question + "?"  # GPT produces better results 
                                        # if there's a question mark.
                                        # using a temp variable so the ? doesn't get cached
    prompt = prompt + "Q: " + temp_question + "\n" 
    response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
            )
    jsonToPython = json.loads(response.last_response.body)
    result = jsonToPython['choices'][0]['text']
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
