# cbot
Cbot is a simple python command line bot based on GPT3. The bot will lookup what the right command line is for natural questions that you ask. A GPT3 API key is required for this to work. 

Example usage:
$> cbot "How do I count the number of lines in a file?"
   wc -l filename.txt

$> cbot "How do I get the mime type of a file?"        
   file filename.txt

$> cbot "How do I create a file with the text 'hello world'"   
   echo hello world > hello.txt

$> cbot "How do I open php in interactive mode?" 
   php -a

$> cbot "How do I set my email using git config?"
   git clone git@github.com:graiz/cbot.git

## Cbot Basics
The application is a simple Python script that prompts GPT3 with a couple examples and the OS of the current system. This helps ensure that Linux, Mac, and Windows specific commands tend to be more accurate.  Cbot is based entirely on GPT3 and it's not perfect. The more examples it has, the better it gets.  If you find examples that improve output or correct mistakes, please feel free to contribute them. 

## Installation
The file needs to be placed in a directory that is accessible within your path. 

$> cbot "What folders are in my path?"
echo $PATH

Also, make sure the file is executable so that you can run it from the command line. 

$> cbot "How do I make cbot.python executable?" 
chmod +x cbot.python

Lastly I'd like to just call the command cbot so I don't have to type the python part of it. 

$> cbot "How do I rename cbot.python to be just cbot?"         
mv cbot.python cbot




