import sys

def main(argc, argv):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    if argc == 2:
        raw_list = argv[1].split(',')
        companies_list = []
        for item in raw_list:
            companies_list.append(item.strip())
        if '' not in companies_list:
            for i in range(len(companies_list)):
                found = False
                for key in COMPANIES.keys():
                    if companies_list[i].upper() == key.upper():
                        ticker = COMPANIES[key]
                        print(str(key) + " stock price is " + str(STOCKS[ticker]))
                        found = True
                for key, value in COMPANIES.items():
                    if companies_list[i].upper() == value.upper():
                        print(str(value) + " is a ticker symbol for " + key)
                        found = True

                if not found:
                    print(companies_list[i] + " is an unknown company or an unknown ticker symbol")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)