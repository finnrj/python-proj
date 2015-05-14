'''
Created on May 14, 2015

@author: finn

Albert and Bernard just became friends with Cheryl, and they want to know when her birtxhday is. 
Cheryl gave them a list of 10 possible dates:

    May 15     May 16     May 19
    June 17    June 18
    July 14    July 16
    August 14  August 15  August 17

Cheryl then tells Albert and Bernard separately the month and the day of the birthday respectively.

1) Albert: I don't know when Cheryl's birthday is, but I know that Bernard does not know too.

2) Bernard: At first I don't know when Cheryl's birthday is, but I know now.

3) Albert: Then I also know when Cheryl's birthday is.

4) So when is Cheryl's birthday?
'''


if __name__ == '__main__':
    candidates = [("May", 15), ("May", 16), ("May", 19),
                  ("June", 17), ("June", 18),
                  ("July", 14), ("July", 16),
                  ("August", 14), ("August", 15), ("August", 17)]
    months = [md[0] for md in candidates]  # set(md[0] for md in candidates)
    days = [md[1] for md in candidates]  # set(md[1] for md in candidates)

    a1 = [md for md in candidates if md[1] in [d for d in days if days.count(d) > 1]]
    a1_excludes = [md for md in candidates if md not in a1]
    b1 = [md for md in a1 if md[0] not in [m[0] for m in a1_excludes] 
          and md[1] in [mdd[1] for mdd in candidates if mdd[0] in [mm[0] for mm in a1_excludes]]]
    a2 = [md for md in b1 if [m[0] for m in b1].count(md[0]) == 1]
    
    print("a1", a1)
    print("a1_excludes", a1_excludes)
    print("b1", b1)
    print("a2", a2)
    
        