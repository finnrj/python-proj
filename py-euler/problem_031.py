'''
In England the currency is made up of pound, £, and pence, p, 
   and there are eight coins in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).

It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?

Others guy solution which looks so smart but I don't understand -.-

public class problem31 {
    final static int TOTAL = 200;

    public static void main(String[] args) {
        int[] coins = {1, 2, 5, 10, 20, 50, 100, 200};
        int[] ways = new int[TOTAL + 1];
        ways[0] = 1;

        for(int coin: coins)
            for(int j = coin; j <= TOTAL; j++)
                ways[j] += ways[j - coin];

        System.out.println("Result: " + ways[TOTAL]);
    }
}

---------------------- Theme: DYNAMIC PROGRAMMING :-D -----------------------
   lets say we have an array: arr of length 201, where arr[i] is the number of
   ways the amount: i can be paid with 1,2 and 5 cent coins. If we also have a 
   coin worth 10 cent, how could we fit it into the array?
   Beginning at index = 10 (coin value) we can now add all the known combinations
   for index = 0 (because we can add a 10 cent coin to each of them). For index = 11
   we can add all known combinations for index = 1 (because we can add a 10 cent coin
   to each of them) and so on......  
----------------------- EO: Theme: DYNAMIC PROGRAMMING :-D ---------------------    
'''


def getCombinations(moneyTaken=0, targetSum=200, coins=[1, 2, 5, 10, 20, 50, 100, 200], i=0):
    if i >= len(coins):
        return 0
    
    if moneyTaken + coins[i] > targetSum:
        return getCombinations(i=i + 1, moneyTaken=moneyTaken)

    if moneyTaken + coins[i] == targetSum:
        return 1 + getCombinations(i=i + 1, moneyTaken=moneyTaken)
   
    
    # moneyTaken < targetSum
    #                        take coin                                        take not
    return getCombinations(i=i, moneyTaken=moneyTaken + coins[i]) + getCombinations(i=i + 1, moneyTaken=moneyTaken)

if __name__ == '__main__':
    print(getCombinations())
    
    
        
        
        
        
