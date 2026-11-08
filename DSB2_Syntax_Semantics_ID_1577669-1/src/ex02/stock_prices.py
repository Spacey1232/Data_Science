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
    if len(argv) == 2:
        argv = [argv[0], argv[1].strip().capitalize()]
        if argv[1] in COMPANIES.keys():
            print(STOCKS[COMPANIES[argv[1]]])
        else:
            print('Unknown company')

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)