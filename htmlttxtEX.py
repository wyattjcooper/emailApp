from bs4 import BeautifulSoup
soup = BeautifulSoup(open(''))
print soup.get_text()