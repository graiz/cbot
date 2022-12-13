# cbot
Cbot is a command line tool that uses GPT-3 to assist users in finding the right command for any given task. With cbot, users can simply type in a brief description of what they want to do, and cbot will use GPT-3 to find the right command to accomplish the task. Cbot makes it easy for users to find the right command quickly, without having to spend time searching through documentation or scrolling through long lists of available commands.



## Installation

To install the cbot utility and set up your GPT-3 API key, follow these steps:
1. Install cbot using the pip command: **pip install cbot-command**
1. Get your GPT-3 API key from https://beta.openai.com/account/api-keys Add your API key to an environmental variable by running the following command, replacing your actual API key: **export OPENAI_API_KEY="YOUR_API_KEY"**
1. If you're using the Bash shell, you can add the above export command to your .bashrc file in your home directory so that it is automatically run every time you open a new terminal. If you're using the Zsh shell, you can add it to your .zshrc file instead.

Once you've completed these steps, cbot will be installed and ready to use. You can run the **cbot "search"** command to search for commands related to a particular topic.


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
The application is a simple Python script that prompts GPT3 with a couple examples and the OS of the current system. This helps ensure that Linux, Mac, and Windows specific commands tend to be more accurate.  Cbot is based entirely on GPT3 and it's not perfect. The more examples it has, the better it gets however the more examples the more GPT3 may cost per request. If you find examples that improve output or correct mistakes, please feel free to contribute them. Future versions of GPT3 will allow training and fine tuning. 

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
Initial version by Gregory Raiz
This code is free to use under the MIT liscense.
