# Should_You_Invest_Into_Meme_Stocks
A look into the hype of "Meme" stocks and whether you should invest
---
# 🐍📈 Should You Invest Into "Meme" Stocks 📉🐍
---
## Members
- Ben McCright aka 👴 Boomer 👴
- Josh Ferguson aka 🦅 Proud Patriot 🇺🇸
- Cole Wood aka 💎 Diamond Hands 👐

# Introduction
 Stocks like Gamestop and AMC have large support communities on social media.  These communities closely monitor the market and then coordinate campaigns with memes, giving rise to the term "meme stock", which garner more support from their followers who amplify and extend their circle of influence.  This tactic gives retail investors a larger voice, and some feel a better chance in the fight against the perceived threat of institutional investors.  Some of the leaders in these campaigns have a mission to hurt short-sellers, but some only want to pump the stock so that they can dump at its highest.  Among the casualties of this "war" are the casual investors who just buy because they see people telling them to on Twitter or Facebook then "hodl" (hold) through the ups and downs.  This study examines the correlation of search interest to stock performance alongside some more conventional, accessible methods of stock selection.  Politics and ethics aside, are these "meme stocks" good investments?

## Method
* Use Google Finance and Alpaca Trading APIs to get historical stock data for each of the 11 sectors in the S & P 500 with select stocks and funds
* Use Google Trends API to get search interest over time for stock tickers
* Use Pandas for Python to clean analyze the data
* Use Panel for Python to display the findings

## Results
![](Images/bb.png)
The far right of this image, late 2020 to current date, shows there can be correlation between search interest and closing price, but it is not a reliable sign to buy.  Often the trend increase is directly over the increase in price, or even slightly lagging it. 
![](Images/algn.png)
Events in the news such as the announcement of the COVID-19 vaccination in October 2020 correlated with a sharp increase in search interest and price of certain stocks in the Healthcare sector.  The analysis does not indicate that meme stocks are sound long-term investments, an investor needs to closely monitor the market and have nuanced understanding of current affairs in order to take advantage of them.
![](Images/time_travel.png)
The SPY fund routinely outperforms nearly every stock in every sector of the S & P 500 but as shown in the Time Traveler tab of the panel, it is possible to beat the SPY fund with "meme stocks", making them good investments in the short term around their trending period.  Until the trend period hits, those same stocks are losing value.
![](Images/heat.gif)
![](Images/box.gif)
Correlation with the S & P 500 index is proportional with beta value of each sector, the mutual fund correlated the most with a mean of 86% across all sectors. The median beta value had higher mean correlation (54%) than the maximum beta value (52%) and minimum beta value (35%).

## Conclusion
Investing in single stocks based on social media campaigns does not provide the security of the conventional investing strategy of having a diversified portfolio of proven performers.  Traditional methods of analyzing historical stock performance and simulating portfolios (examples below) are more useful for someone looking to make long-term investments.  If someone is a casual investor or has a low threshold for risk or loss, they are better off investing in a carefully managed fund like SPY or a sector-specific mutual fund.
![](Images/stonks.webp)

## Additional Data Visualizations
![](Images/trend.gif)
![](Images/candlestick.png)
![](Images/spy.gif)
![](Images/tt.gif)
![](Images/sharpe.gif)

## References
* [Plotly Express](https://plotly.com/python/plotly-express/)
* [Plotly Graph Objects in Python](https://plotly.com/python/graph-objects/)
* [Panel for Python](https://panel.holoviz.org/)
* [Google Trends API for Python](https://pypi.org/project/pytrends/)
* [Alpaca Trading API](https://alpaca.markets/docs/)
* [SPY Fund](https://www.ssga.com/us/en/institutional/etfs/funds/spdr-sp-500-etf-trust-spy)