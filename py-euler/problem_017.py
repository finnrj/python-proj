'''
Created on Jun 2, 2015

@author: finn


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two)
contains 23 letters and 115 (one hundred and fifteen) contains 20 letters.
The use of "and" when writing out numbers is in compliance with British usage.

'''
        
if __name__ == '__main__':
    oneDigit = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen"]
    decems = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    hundredCount = len("hundred")
    thousandCount = len("thousand")
    
    oneDigitCount = sum([len(i) for i in oneDigit])
    teensCount = sum([len(i) for i in teens])
    decemsCount = sum([(10 * len(i)) + oneDigitCount for i in decems])
    
    # 1-99
    oneTo99 = oneDigitCount + teensCount + decemsCount
    print("total 1-99:", oneTo99)
    hunn = [(len(h) + hundredCount) * 100 + len("and") * 99 + oneTo99 for h in oneDigit]
    print("1-1000:", oneTo99 + sum(hunn) + len(oneDigit[0]) + thousandCount)
