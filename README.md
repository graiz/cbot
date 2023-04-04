# cbot
Cbot is a simple python command line bot that uses the gpt-3.5-turbo endpoint from OpenAI. The bot will lookup what the right command line is for natural questions that you ask. An OpenAI API key is required for this to work. 

## Example usage:
```
$> cbot "How do I count the number of lines in a file?"
   wc -l filename.txt

$> cbot "How do I get the mime type of a file?"        
   file filename.txt

$> cbot "How do I create a file with the text 'hello world'"   
   echo hello world > hello.txt

$> cbot "How do I open php in interactive mode?" 
   php -a

$> cbot "How do I set my email using git config?"
   git config --global user.email "new_email@address.com"

$> cbot What is the current date
   date
```
Note: That you don't have to use quotes, however if you do
   this you can not include a question mark because the shell
   will try to match it with a file.

Use the -x option to execute the command.
```
$> cbot -x How do I create a file test.txt
   touch test.txt"

```

## Cbot Basics
The application is a simple Python script that prompts GPT3.5 with a system message and the OS of the current system. This helps ensure that Linux, Mac, and Windows specific commands tend to be more accurate.  Cbot is based entirely on GPT3.5 and it's not perfect. Currently cbot does not have a context for it's responses, so each response cannot reference previous responses. 

## Installation

- Add your OpenAI API key into an environmental variable. The easiest way to do this is to add to to your command line shell by adding the line:  export OPENAI_API_KEY="then_enter_your_key"
This is most commonly a file called .zshrc or .bashrc in your home directory.  The API key is something that you can get from: https://beta.openai.com/account/api-keyse

- Clone this repo to your computer using the command line.
- Allow the file to be executed and then copy the cbot.python file into a directory that is accessible within your path. It is recommended that you name it "cbot" without the python extension for simplicity. 
- You will also need to make sure that python has the OpenAI mobule.  
```
$> git clone git@github.com:graiz/cbot.git
$> cd cbot
$> chmod +x cbot.py
$> mv cbot.py ~/bin/cbot      (you can use a different location in your $PATH)
$> pip3 install openai
$> pip3 install pyperclip    
```
## Testing

If everything is working you should be able to run "cbot" from the command line with a question and it'll return an answer.

# Advanced tricks...

If you're feeling adventurous you can pass the command option **-x** to execute the command. Be careful as this will execute whatever is passed back from GPT3. Using this with simple things may be fine but this is not recommended with any actions that could be destructive.

> **Note:** The **-x** option will go ahead and run the command returned without asking.  Proceed with caution, for added safety sudo commands will not be automatically run.

You can also call cbot with a **-s** option. This will save any command as a shortcut with whatever name you choose. The first parameter is the name of the command and the second is the command itself in quotes. 
```
$> cbot -s nap "pmset sleepnow"
   Saving shortcut nap, will return: pmset sleepnow
$> cbot -x nap
   Sleeping now...
```

To copy a command directly into the clipboard use the **-c** option. Can be useful if you want to execute the command but you don't trust cbot to do so automatically. 

Cbot has a -g option to ask general questions. The results when you ask a general question will not be formated as a command line. This is useful for asking general questions, historical facts or other information not likely to be formated as a command. 
```
$> cbot -g "Who was the 23rd president?"
  Herbert Hoover  
$> cbot -g "What is the meaning of life?"p
   42
```


Cbot saves every command in a SQLite3 database located in the home directory .cbot_cache. You can inspect or delete this directory, you can also directly add or remove shortcuts if needed.



#### Credits
----
Current version by Roberto Delgado
Initial version by Gregory Raiz
This code is free to use under the MIT liscense.
