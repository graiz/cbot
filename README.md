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

## Cbot Basics
The application is a simple Python script that prompts GPT3 with a couple examples and the OS of the current system. This helps ensure that Linux, Mac, and Windows specific commands tend to be more accurate.  Cbot is based entirely on GPT3 and it's not perfect. The more examples it has, the better it gets.  If you find examples that improve output or correct mistakes, please feel free to contribute them. 
