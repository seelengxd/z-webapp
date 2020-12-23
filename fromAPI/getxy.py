import json
import time
import os
from selenium import webdriver
#https://developers.onemap.sg/commonapi/search?searchVal=680001&returnGeom=Y&getAddrDetails=N&pageNum=1

# resp = requests.post('https://developers.onemap.sg/privateapi/auth/post/getToken', data={'email':'seeleng200212@gmail.com', 'password':'whatever'})
# print(resp.text)
# print(resp.json())

chromedriver_location = os.path.join(os.getcwd(), '..', chromedriver)
driver = webdriver.Chrome(chromedriver_location)

store = {}
for i in range(8, 83):
    for j in range(0, 100):
        try:
            query = f'{i:0>2}0{j:0>2}1'
        # payload = {'searchVal':query, 'returnGeom':'Y', 'getAddrDetails':'N', 'pageNum':'1'}
            url = f'https://developers.onemap.sg/commonapi/search?searchVal={query}&returnGeom=Y&getAddrDetails=Y&pageNum=1'
            driver.get(url)
            time.sleep(0.3)
            s = driver.find_element_by_tag_name("pre").text
            data = json.loads(s)
            if data['found']:
                store[query] = [float(data['results'][0]['LATITUDE']), float(data['results'][0]['LONGITUDE'])]
                break
        except:
            time.sleep(5)

with open('xy.json', 'w') as f:
    json.dump(store, f, indent=4)

driver.close()
