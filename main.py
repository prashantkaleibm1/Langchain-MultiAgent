import src
from src.tools.tools import scrape_url,web_search
#output=web_search("Latest news on Saudi Arabia")
#print(output)
#result=scrape_url("https://www.thehindubusinessline.com/markets/angel-ones-consolidated-pat-up-582-y-o-y-in-september-quarter/article71588673.ece")
result=web_search.invoke("Latest news on Saudi Arabia")   # @tool decorator defined for function
print(result)