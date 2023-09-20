import requests
from bs4 import BeautifulSoup
import re
from real_bank import Real_bank
class main():
    def __init__(self):
        self.l2 = []
        self.l4 = []

    def parse_rate(self):
        l = []
        req = requests.get('https://10bestpersonalloans.com/go/bank_competitors_rates-usa-eng-d-g.html')
        soup = BeautifulSoup(req.text, "html.parser")
        percentage = soup.find_all('span')
        for i in percentage:
            text = i.get_text()
            if '%' in text:
                apr = text.strip()
                l.append(apr)
        (list(set(l)))
        l2 = []
        for j in l:
            a1 = j[j.find('APR: ') + len('APR: '): j.rfind('% -')]
            a2 = j[j.find(' - ') + len(' - '): j.rfind('%')]
            avg_val = f'{(float(a1) + float(a2)) / 2: .2f}'
            l2.append(avg_val)
        l2 = list(set(l2))
        return(l2)


    def parse_name(self):
        req = requests.get('https://10bestpersonalloans.com/go/bank_competitors_rates-usa-eng-d-g.html')
        soup = BeautifulSoup(req.text, "html.parser")
        l3 = []
        l4 = []
        names = soup.find_all('span', {'class': 'Card1_simpleText__S5PZY'})
        for n in names:
            tag = re.findall(re.escape('>') + "(.*)" + re.escape('<'), str(n))[0]
            l3.append(tag)
        for m in l3:
            if 'Visit' in m:
                m = m[6:]
                l4.append(m)
            else:
                m = 'A Company ' + m
                l4.append(m)
        del l4[len(self.l2)-1:]
        return(l4)

def getBanks():
    rates = main().parse_rate()
    names = main().parse_name()

    banks = []
    for i in range(0, len(rates)):
        banks.append(Real_bank(names[i],rates[i]))
    return banks
if __name__ == '__main__':
    banks = getBanks()
    for bank in banks:
        print(bank.getName())
        print(bank.getRate())