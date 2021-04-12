# cbot
Cbot is a simple python command line bot based on GPT3. The bot will lookup what the right command line is for natural questions that you ask. A GPT3 API key is required for this to work. 

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

$> cbot -x "What version of python am I using?"
   cbot executing:python -V
   Python 3.8.2
```

## Cbot Basics
The application is a simple Python script that prompts GPT3 with a couple examples and the OS of the current system. This helps ensure that Linux, Mac, and Windows specific commands tend to be more accurate.  Cbot is based entirely on GPT3 and it's not perfect. The more examples it has, the better it gets however the more examples the more GPT3 may cost per request. If you find examples that improve output or correct mistakes, please feel free to contribute them. Future versions of GPT3 will allow training and fine tuning. 

## Installation

- Clone this repo to your computer using the command line: 
  $> git clone git@github.com:graiz/cbot.git

- Add your GPT3 API key into an environmental variable. The easiest way to do this is to add to to your command line shell by adding the line:  export OPENAI_API_KEY="then_enter_your_key"
This is most commonly a file called .zshrc or .bashrc in your home directory.  The API key is something that you can get from: https://beta.openai.com/account/api-keyse

- Once the key is set you will want to copy the cbot.python file into a directory that is accessible within your path.  
- It is recommended to rename it as just "cbot" without the python extension for simplicity and allow the file to be executed.
- You will also need to make sure that python has the OpenAI mobule.  
```
$> chmod +x cbot.python
$> mv cbot.python ~/bin/cbot
$> pip3 install openai
```
## Testing

If everything is working you should be able to run "cbot" from the command line with a question and it'll return an answer.

# Advanced tricks...

If you're feeling adventurous you can pass the command option **-x** to execute the command. Be careful as this will execute whatever is passed back from GPT3. Using this with simple things may be fine but this is not recommended with any actions that could be destructive.

> **Note:** The **-x** option will go ahead and run the command returned without asking.  Proceed with caution.


#### Credits
----
Initial version by Gregory Raiz
This code is free to use under the MIT liscense.
