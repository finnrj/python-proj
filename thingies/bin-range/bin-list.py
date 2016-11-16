#! /home/finn/tmp/anaconda3/bin/python3

ZEROS = 11 * "0"
NINES = 11 * "9"

def makeBeginning(number):
    return float((number + ZEROS)[:11])

def makeEnd(number):
    return float((number + NINES)[:11]) + 1.5

def makeCardtype2RangeBorder(lines):
    result = {}
    for l in lines:
        cardtype = l[1].strip().upper()
        accumulator = result.get(cardtype, [])
        accumulator.append((makeBeginning(l[0]), l[3]))
        accumulator.append((makeEnd(l[0]), l[3]))
        result.setdefault(cardtype, accumulator)
    return result

def isBeginningOfRange(borderValue):
    return str(borderValue).endswith("0")

def compactRanges(cardtype, rangeBorders):
    country2counter = {}
    compactedRanges = []
    maxCount = (0, '')
    rangeBorders.sort()
    countryStack = []
    for border in rangeBorders:
        print("countrystack: " + str(countryStack))
        borderValue = border[0]
        country = border[1]
        if isBeginningOfRange(borderValue):
            counter = country2counter.get(country, (0, borderValue))
            newCount = counter[0] + 1
            if newCount == 1: # new range begin for this country
                country2counter[country] = (newCount, borderValue)
                if len(countryStack) > 0 : # at least one other country range was started
                    previousCountry = countryStack[-1]
                    counter = country2counter.get(previousCountry)
                    print("appending at range beginning: " + str((counter[1], borderValue - 1, cardtype, previousCountry))) 
                    compactedRanges.append((counter[1], borderValue - 1, cardtype, previousCountry)) # end the started range
            else: # at least one range is already started for this country
                previousCountry = countryStack[-1] # country stack cannot be empty
                if previousCountry == country:
                    country2counter[country] = (newCount, counter[1])
                else: # end the started range for the previous country
                    country2counter[country] = (newCount, borderValue)
                    previousCounter = country2counter.get(previousCountry)
                    print("appending at range beginning: " + str((previousCounter[1], borderValue - 1, cardtype, previousCountry))) 
                    compactedRanges.append((previousCounter[1], borderValue - 1, cardtype, previousCountry)) # end the started range
            countryStack.append(country)
            if newCount > maxCount[0]:
                maxCount = (newCount, country)
        else: # it is a range end
            if not country in country2counter.keys():
                print("Houston - we've got a border problem: " + str(border))
                exit(1)
            counter = country2counter.get(country)
            newCount = counter[0] - 1
            if newCount == 0: # we might have to finish a range for this country
                if countryStack[-1] == country: # country stack cannot be empty
                    print("appending at range end: " + str((counter[1], borderValue - 1.5, cardtype, country))) 
                    compactedRanges.append((counter[1], borderValue - 1.5, cardtype, country))
                    if len(countryStack) > 1 and not countryStack[-2] == country: # restart range for this country
                        country2counter[countryStack[-2]] = (country2counter.get(countryStack[-2])[0], borderValue - 0.5) 
                del(country2counter[country])
            else: # the range is not finished for this country yet
                if not countryStack[-2] == country: # finish this range
                    print("appending at range end: " + str((counter[1], borderValue - 1.5, cardtype, country))) 
                    compactedRanges.append((counter[1], borderValue - 1.5, cardtype, country))
                    if len(countryStack) > 1 and not countryStack[-2] == country: # restart range for this country
                        country2counter[countryStack[-2]] = (country2counter.get(countryStack[-2])[0], borderValue - 0.5) 
                country2counter[country] = (newCount, counter[1])
            countryStack.pop(lastIndex(countryStack, country))
    if not len(country2counter.keys()) == 0:
        print("Houston - we've got a dict problem: " + str(country2counter))
        exit(1)
    print("maximum number of consecutive ranges for cardtype: %s" % cardtype)
    print("%d for country: %s" % maxCount)
    return compactedRanges

def lastIndex(lst, target):
    return len(lst) - 1 - list(reversed(lst)).index(target)

import unittest
class bin_list_test(unittest.TestCase):

    def testOneRange(self):
        country = "USA"
        rangeBorders = []
        rangeBorders.append((makeBeginning("180"), country))
        rangeBorders.append((makeEnd("180"), country))
        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 1)

    def testTwoDisjointRanges(self):
        country = "USA"
        rangeBorders = []
        rangeBorders.append((makeBeginning("180"), country))
        rangeBorders.append((makeEnd("180"), country))

        rangeBorders.append((makeBeginning("195"), country))
        rangeBorders.append((makeEnd("195"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 2)

    def testTwoDisjointRanges(self):
        country = "USA"
        rangeBorders = []
        rangeBorders.append((makeBeginning("180"), country))
        rangeBorders.append((makeEnd("180"), country))

        rangeBorders.append((makeBeginning("195"), country))
        rangeBorders.append((makeEnd("195"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 2)

    def testTwoAdjointRanges(self):
        country = "USA"
        rangeBorders = []
        rangeBorders.append((makeBeginning("180"), country))
        rangeBorders.append((makeEnd("180"), country))

        rangeBorders.append((makeBeginning("181"), country))
        rangeBorders.append((makeEnd("181"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 1)

    def testTwoAdjointRangesDifferentCountries(self):
        country = "US"
        rangeBorders = []
        rangeBorders.append((makeBeginning("180"), country))
        rangeBorders.append((makeEnd("180"), country))

        country = "DE"
        rangeBorders.append((makeBeginning("181"), country))
        rangeBorders.append((makeEnd("181"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 2)

    def testCompleteOverlappingRanges(self):
        country = "USA"
        rangeBorders = []
        rangeBorders.append((makeBeginning("18"), country))
        rangeBorders.append((makeEnd("18"), country))

        rangeBorders.append((makeBeginning("181"), country))
        rangeBorders.append((makeEnd("181"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 1)
        binRange = result[0]
        self.assertEqual (binRange[0], 18000000000)
        self.assertEqual (binRange[1], 18999999999)

    def testCompleteOverlappingRangesDifferentCountries(self):
        country = "US"
        rangeBorders = []
        rangeBorders.append((makeBeginning("18"), country))
        rangeBorders.append((makeEnd("18"), country))

        country = "DE"
        rangeBorders.append((makeBeginning("181"), country))
        rangeBorders.append((makeEnd("181"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 3)
        binRangeUS = result[0]
        binRangeDE = result[1]
        binRangeUS_2 = result[2]
        self.assertEqual (binRangeUS[0], 18000000000)
        self.assertEqual (binRangeUS[1], 18099999999)
        self.assertEqual (binRangeDE[0], 18100000000)
        self.assertEqual (binRangeDE[1], 18199999999)
        self.assertEqual (binRangeUS_2[0], 18200000000)
        self.assertEqual (binRangeUS_2[1], 18999999999)

    def testCompleteOverlappingRangesManyCountries(self):
        country = "US"
        rangeBorders = []
        rangeBorders.append((makeBeginning("18"), country))
        rangeBorders.append((makeEnd("18"), country))

        country = "DE"
        rangeBorders.append((makeBeginning("181"), country))
        rangeBorders.append((makeEnd("181"), country))

        country = "US"
        rangeBorders.append((makeBeginning("1815"), country))
        rangeBorders.append((makeEnd("1815"), country))

        country = "PH"
        rangeBorders.append((makeBeginning("18153"), country))
        rangeBorders.append((makeEnd("18153"), country))

        result = compactRanges("MS", rangeBorders)
        self.assertEqual (len(result), 7)
        binRangeUS_1 = result[0]
        binRangeDE_1 = result[1]
        binRangeUS_2 = result[2]
        binRangePH_1 = result[3]
        binRangeUS_3 = result[4]
        binRangeDE_2 = result[5]
        binRangeUS_4 = result[6]
        self.assertEqual (binRangeUS_1[0], 18000000000)
        self.assertEqual (binRangeUS_1[1], 18099999999)
        self.assertEqual (binRangeDE_1[0], 18100000000)
        self.assertEqual (binRangeDE_1[1], 18149999999)
        self.assertEqual (binRangeUS_2[0], 18150000000)
        self.assertEqual (binRangeUS_2[1], 18152999999)
        self.assertEqual (binRangePH_1[0], 18153000000)
        self.assertEqual (binRangePH_1[1], 18153999999)
        self.assertEqual (binRangeUS_3[0], 18154000000)
        self.assertEqual (binRangeUS_3[1], 18159999999)
        self.assertEqual (binRangeDE_2[0], 18160000000)
        self.assertEqual (binRangeDE_2[1], 18199999999)
        self.assertEqual (binRangeUS_4[0], 18200000000)
        self.assertEqual (binRangeUS_4[1], 18999999999)


if __name__ == '__main__':
    unittest.main()
    
    # lines = [line.split(';')[:4] for line in open('/home/finn/python/misc/bin_liste_concardis_gesamt-20160902.csv', encoding='latin-1', errors='ignore').readlines()[1:]]
    # linesCount = len(lines)
    # print("bin lines read: %d" % linesCount)
    # cardtype2rangeBorder = makeCardtype2RangeBorder(lines)
    # # print(list((cardtype,  cardtype2rangeBorder[cardtype][:5]) for cardtype in CARDTYPES))
    # CARDTYPES = cardtype2rangeBorder.keys()
    # print("cardtype :  count")
    # for cardtype in CARDTYPES:
    #     print("%5s    :%7d" % (cardtype, len(cardtype2rangeBorder[cardtype])//2))
    # print()

    # for cardtype in CARDTYPES:
    #     cardtype2rangeBorder[cardtype] = compactRanges(cardtype, cardtype2rangeBorder[cardtype])

    # rangeCount = sum(len(cardtype2rangeBorder[cardtype]) for cardtype in CARDTYPES)
    # print("\nAfter contraction of ranges:")
    # print("range count: %d" % rangeCount) 
    # print("cardtype :  count")
    # for cardtype in CARDTYPES:
    #     print("%5s    :%7d" % (cardtype, len(cardtype2rangeBorder[cardtype])//2))

    # print("contraction in %% = %0.2f%%" % (100 - (rangeCount/linesCount * 100)))
    # print()
    
