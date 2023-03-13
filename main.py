import requests
from bs4 import BeautifulSoup
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt


source = requests.get('https://www.weather.go.kr/weather/observation/currentweather.jsp')
soup = BeautifulSoup(source.content,"html.parser")

table = soup.find('table',{'id':'weather_table'})
data = []

print("#"*30)
print("\n오늘 전국의 날씨 상황을 전해드리겠습니다!\n")
print("#"*30)

print("\n지역    현재 기온    습도")

for tr in table.find_all('tr'):
    tds = list(tr.find_all('td'))
    for td in tds:
        if td.find('a'):
            point = td.find('a').text
            temp = tds[5].text
            humidity = tds[10].text
            print("{0:<7} {1:<7} {2:<7}".format(point,temp,humidity))
            data.append([point,temp,humidity])
print("\n")
print("-"*30)
print("\n 날씨였습니다!\n")
print("-"*30)

with open('weather.csv','w') as f:
    f.write('지역, 온도, 습도\n')
    for i in data:
        f.write('{0},{1},{2}\n'.format(i[0],i[1],i[2]))

df = pandas.read_csv('weather.csv', index_col='지역' , encoding='euc-kr')

city_df = df.loc[['서울','세종','대전','인천','대구','광주','부산','울산']]

font_name = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\malgun.ttf').get_name()
mpl.rc('font',family=font_name)

ax = city_df.plot(kind='bar',title='날씨',figsize=(20,4),legend=True,fontsize=15)
ax.set_xlabel('도시',fontsize=20)
ax.set_ylabel('기온/습도',fontsize=20)
ax.legend(['기온','습도'],fontsize=20)

plt.show()