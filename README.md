# final_project


*1.What is your group's name?

Lauren & Shrinali

*2.Who are you working with?

Lauren Lunsford and Shrinali Patel

*3.What APIs will you be gathering data from?

Twitter & Urban Dictionary (Lauren has twitter access)

*4.What data will you collect from each API and store in a database? / 5.What data will you be calculating from the data in the database?

Goal is to access the twitter API and collect English tweets in the Ann Arbor area over a period of 3 days.

We’d create a dictionary of words from these tweets.
 
We’d then collect 3 days of tweets 3 weeks later and identify words that increase in frequency.

Those words would be labelled “slang”. (since we’re only using 2 time slices, we’d likely not include words that had 0 mentions in the first instance as a way to avoid an infinite frequency increase)

Then we’d search through Urban Dictionary API to see if we can pull the definition of those slang words.
We’d then display the 5 words with the largest slang  
 
*6.What visualization package will you be using (matplotlib, plotly, seaborn, etc)?  

GGplot 

7. What graphs/charts will you be creating?
Graphic of slang frequencies of the top 10 slang words in the Ann Arbor area
We’ll be showing the baseline frequencies at each point in time, and the slope of the frequencies (fastest growing slang). 
 
 
Backup:
 
If we’re unable to pull old tweets or there is a cost associated with doing so that is above $10, we’ll update our plan.
 
Goal:
1. To access the twitter API and collect English tweets in the Ann Arbor area over a period of 3 days.
2. We’d create a dictionary of words from these tweets.
3. We’d use a common list of 1000 most frequent words in the English language and erase all words in our dictionary 
4. We’d then use the remaining words with more than 1 instance (to avoid spelling errors) and would pull data from a dictionary API to attach definitions to those words.  This would identify region specific phrases (oop, umich, UM, squirrels, etc.).
5. We’d represent it similarly
