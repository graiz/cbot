#!/usr/bin/env python3
import os
from openai import OpenAI

client = OpenAI()
import sys
import sqlite3
import subprocess
import pyperclip

def initDB():
    from os.path import expanduser
    home = expanduser("~")
    global cache
    try:
        cache = sqlite3.connect(home + "/.cbot_cache")
        cache.execute("""
                        CREATE TABLE IF NOT EXISTS questions
                        (id INTEGER PRIMARY KEY,
                        question TEXT,
                        answer TEXT,
                        count INTEGER DEFAULT 1)""")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print("Failed to initialize cache database.")
        exit(1)

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
    global interactive
    shortcut = ""
    execute = False
    clip = False
    interactive = False
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
        cbot -i                                   (interactive shell mode)
        """)
        exit()

    if "-i" in question:
        interactive = True
        question_mode = "interactive"
        return ""

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
        if len(sys.argv) < 4:
            print("Error: -s flag requires two arguments: shortcut name and command")
            print("Example: cbot -s nap 'pmset sleepnow'")
            exit(1)
        question = sys.argv[2]
        shortcut = sys.argv[3]

    return question

def interactive_mode(platform):
    """Interactive shell mode - execute commands conversationally"""
    # ANSI color codes
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    print("🤖 Cbot Interactive Mode")
    print("Type your commands naturally. Type 'exit' or 'quit' to leave.\n")

    # Initialize database for caching
    initDB()

    conversation_history = []

    while True:
        try:
            # Get current directory and display in prompt
            cwd = os.getcwd()

            # Smart path display: basename only, except for special dirs
            if cwd == os.path.expanduser("~"):
                display_path = "~"
            elif cwd == "/":
                display_path = "/"
            else:
                display_path = os.path.basename(cwd)

            # Get user input with colored directory prompt
            user_input = input(f"{CYAN}{display_path}{RESET} ➜ Me> ").strip()

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Build context from conversation history
            context = f"Current directory: {os.getcwd()}\n\n"
            if conversation_history:
                context += "Recent conversation and command outputs:\n"
                for item in conversation_history:
                    context += f"{item}\n"
                context += "\n"

            # Check cache first
            cache_key = f"interactive:{user_input}"
            cached_command = checkQ(cache_key)

            if cached_command:
                command = cached_command
                print(f"{BLUE}💾{RESET} {GREEN}cbot>{RESET} {command}")
            else:
                # Create prompt for command generation
                input_text = f"""{context}You are a {platform} command line expert in an interactive shell session. The user will make natural language requests.

IMPORTANT: Use the conversation history above to understand context. If the user refers to files, directories, or data from previous outputs (e.g., "the latest", "that file", "those PDFs"), look at the Output sections above to find the exact names and paths.

For each request:
1. CHECK THE RECENT OUTPUTS ABOVE for context - file names, paths, data that the user is referring to
2. Determine the exact command to run based on that context
3. Interactive commands are allowed - the user can respond to prompts (e.g., rm -i is fine, vim is fine, python REPL is fine)
4. If the command output might be longer than one screen (like 'ls -la' in large directories, 'cat' large files, 'ps aux', etc.), pipe it through 'more' or 'less' for pagination
5. Respond with ONLY the command, no explanations, no markdown, no formatting

Current request: {user_input}"""

                # Call GPT-5-mini
                try:
                    response = client.responses.create(
                        model="gpt-5-mini",
                        input=input_text,
                        max_output_tokens=100,
                        reasoning={"effort": "minimal"}
                    )
                    command = response.output_text.strip()

                    # Store in cache
                    insertQ(cache_key, command)

                    # Execute the command (display in green)
                    print(f"{GREEN}cbot>{RESET} {command}")
                except AttributeError as e:
                    if "has no attribute 'responses'" in str(e):
                        print(f"⚠️  Error: OpenAI library version too old. Please upgrade: pip install --upgrade 'openai>=2.0.0'")
                    else:
                        print(f"⚠️  Error: {e}")
                    continue
                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg or "401" in error_msg:
                        print(f"⚠️  Error: Invalid or missing OpenAI API key. Set OPENAI_API_KEY environment variable.")
                    else:
                        print(f"⚠️  Error calling API: {e}")
                    continue

            # Execute the command (whether from cache or API)
            # Special handling for cd commands - change the actual Python working directory
            if command.strip().startswith('cd '):
                try:
                    # Extract the directory path
                    cd_path = command.strip()[3:].strip()
                    # Expand ~ and environment variables
                    cd_path = os.path.expanduser(cd_path)
                    cd_path = os.path.expandvars(cd_path)
                    # Change directory
                    os.chdir(cd_path)
                except FileNotFoundError:
                    print(f"cd: no such file or directory: {cd_path}")
                except NotADirectoryError:
                    print(f"cd: not a directory: {cd_path}")
                except PermissionError:
                    print(f"cd: permission denied: {cd_path}")
                except Exception as e:
                    print(f"cd: {e}")
            else:
                # Run without capturing output to allow interactive commands
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        timeout=300  # 5 minute timeout for interactive commands
                    )
                except subprocess.TimeoutExpired:
                    print("⚠️  Command timed out (5 minute limit)")
                except Exception as e:
                    print(f"⚠️  Error executing command: {e}")

            # Add to conversation history (no output since we didn't capture it)
            conversation_history.append(f"User: {user_input}")
            conversation_history.append(f"Command: {command}")

            # Trim conversation history to last 1000 characters total
            history_text = '\n'.join(conversation_history)
            if len(history_text) > 1000:
                # Keep trimming from the beginning until we're under 1000 chars
                while len('\n'.join(conversation_history)) > 1000 and len(conversation_history) > 1:
                    conversation_history.pop(0)
                # If still too long, truncate the oldest entry
                if len('\n'.join(conversation_history)) > 1000:
                    conversation_history[0] = "..." + '\n'.join(conversation_history)[-1000:]

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

    # Close database connection
    closeDB()

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

    # Handle interactive mode
    if question_mode == "interactive":
        interactive_mode(platform)
        return

    initDB()

    if question_mode == "shortcut":
        insertQ(question, shortcut)
        print("Saving Shortcut")
        cache_answer = False
    else:
        cache_answer = checkQ(question)

    if not cache_answer and question_mode in ["general", "normal"]:
        # Build the input prompt based on mode
        if question_mode == "general":
            input_text = question
        else:
            # For command mode, provide clear instructions for raw output
            input_text = f"You are a {platform} command line expert. Provide ONLY the exact command to execute for this request, with no explanations, no markdown formatting, no code blocks. Just the raw command.\n\nRequest: {question}"

        try:
            # Using gpt-5-mini with Responses API (does not support temperature parameter)
            response = client.responses.create(
                model="gpt-5-mini",
                input=input_text,
                max_output_tokens=100,  # Minimum is 16
                reasoning={"effort": "minimal"}
            )
            result = response.output_text.strip()
            insertQ(question, result)
        except AttributeError as e:
            if "has no attribute 'responses'" in str(e):
                print(f"Error: Your OpenAI library version is too old.")
                print(f"Please upgrade: pip install --upgrade 'openai>=2.0.0'")
            else:
                print(f"Error: {e}")
            closeDB()
            exit(1)
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "Incorrect API key" in error_msg or "401" in error_msg:
                print(f"Error: Invalid or missing OpenAI API key.")
                print("Please set your OPENAI_API_KEY environment variable.")
                print("Get your API key at: https://platform.openai.com/account/api-keys")
            else:
                print(f"Error calling OpenAI API: {e}")
                print("Please check your internet connection.")
            closeDB()
            exit(1)
    else:
        result = cache_answer
        if question_mode != "shortcut":
            print("💾 Cache Hit")

    if clip:
        try:
            pyperclip.copy(result)
            print("✓ Copied to clipboard")
        except Exception as e:
            print(f"Warning: Could not copy to clipboard: {e}")
    if execute:
        print(f"cbot executing: {result}")
        if "sudo" in result:
            print("Execution canceled, cbot will not execute sudo commands.")
        else:
            try:
                subprocess.run(result, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
            except Exception as e:
                print(f"Error executing command: {e}")
    else:
        if question_mode != "shortcut":
            print(result)

    closeDB()

if __name__ == "__main__":
    sys.exit(main())
