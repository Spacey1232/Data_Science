#!/usr/bin/env python3

import timeit

def base_method(emails):
    result=[]
    for email in emails:
        if "@gmail" in email:
            result.append(email)
    return result
def senond_variant(emails):
    result = [email for email in emails if "@gmail" in email]
    return result

def main():
    emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
        ] * 5
    
    time1=timeit.timeit(lambda:
                        base_method(emails),
                        number=90_000_000)
    time2=timeit.timeit(lambda:
                        senond_variant(emails),
                        number=90_000_000)
    if time2 <= time1:
        print("It is better to use a list comprehension")
    else:
        print("It is better to use a loop")
    print(min(time1,time2),"vs", max(time1,time2))
if __name__=="__main__":
    main()

