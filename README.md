# MrkChn-0.1
my first mini simple program on python for fun.  
generating text based on markov chain  
~~pls dont read that shit!!~~  

![image](material\image1.png)

## How to use:
> clone the repo or download exe from releases  
> in path executable file put any txt file with text  
> after first file start, code create config.ini file  
### config.ini
* seed - first word in generated text, default value is <START>
* text_len - text lenght yeah
* txt_filename - original text file for markov chain
* json_dump - saving dumped json model; bool
* json_filename - saving dumped model in this file if json_dump is true
* gen_num - count of generation for one time
* launguage - idk, mb in feature

**how values of config.ini are parsed you can find in classes/ConfigParser.py**
