from http_fns import simple_get
from bs4 import BeautifulSoup

raw_html = simple_get('http://192.168.2.1/index.html')
#print( len(raw_html) )

html = BeautifulSoup(raw_html, 'html.parser')
status = html.find('li', id='batteryImg')
#.attrs['class'][0]

print(status)
