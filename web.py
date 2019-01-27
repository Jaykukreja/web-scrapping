import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
import re

#from urllib.request import urlopen
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
#from urllib2 import urlopen
'''try:
    from urllib.request  import urlopen
except ImportError:
    from urllib2 import urlopen'''
from bs4 import BeautifulSoup
url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)
print("k")
soup = BeautifulSoup(html, 'lxml') #The Beautiful Soup package is used to parse the html, that is, take the raw html text and break it into Python objects
#print("j")
#print(type(soup))
#print(html.read())
title = soup.title
#print(title)
all_links = soup.find_all("a")
#print(all_links)
'''for link in all_links:
    print(link.get("href"))'''
rows = soup.find_all('tr')
#print(rows[:10])
'''for row in rows:
    row_td = row.find_all('td')
print(row_td)
print(type(row_td))

str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)'''


list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
#print(clean2)
#print(type(clean2))
#print(list_rows)
df = pd.DataFrame(list_rows)
#print(df.head(10))

df1 = df[0].str.split(',', expand=True)
#print(df1.head(10))

df1[0] = df1[0].str.strip('[')
df1[0] = df1[0].str.strip(']')


#print(df1.head(10))

col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
#print(all_header)
df2 = pd.DataFrame(all_header)
#print("l")
#print(df2.head()) 
df3 = df2[0].str.split(',', expand=True)
#print(df3.head())


frames = [df3, df1]

df4 = pd.concat(frames)
print(df4.head(10))

df5 = df4.rename(columns=df4.iloc[0])
print(df5.head(10))

df5.info()
print("d5")
print(df5.shape)   #kitna number of columns and rows
df6 = df5.dropna(axis=0, how='any')



print("d6")

df7 = df6.drop(df6.index[0])

print(df7.head(10))

time_list = df7[' Chip Time'].tolist()

# You can use a for loop to convert 'Chip Time' to minutes

time_mins = []
for i in time_list:
    h, m, s = i.split(':')
    math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    time_mins.append(math)
print(time_mins)

df7['Runner_mins'] = time_mins
print(df7.head())
'''df7.describe(include=[np.number])
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5
df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])
([<matplotlib.axis.XTick at 0x570dd106d8>],
 <a list of 1 Text xticklabel objects>)

x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()'''