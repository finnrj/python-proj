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

'''

coinsPrime = [1, 2, 5, 10, 20, 50, 100, 200]
coins = coinsPrime[::-1]

targetSum = 200

def helper(i, s):
    if i >= len(coins):
        return 0
    
    if s + coins[i] == 200:
        return 1 + helper(i + 1, s)
    
    if s + coins[i] > 200:
        return helper(i + 1, s)
    
    # s < targetSum
    #                    take coin    take not
    return helper(i, s + coins[i]) + helper(i + 1, s)

if __name__ == '__main__':
    print(helper(0, 0))
    
    
        
        
        
        
