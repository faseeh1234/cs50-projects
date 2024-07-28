import cs50
import math

# only accept if money is greater than 0
while True:
    money = cs50.get_float("Enter change: ")
    if money > 0:
        break
# Ensure dollars converted to cents + initiate all variables
money = money * 100
quarters = 0
dimes = 0
nickels = 0
cents = 0
coins = 0
# Calculate each coin's value and subtract from our total number of cents
quarters = math.floor(money / 25)
money = money - (25 * quarters)
dimes = math.floor(money / 10)
money = money - (10 * dimes)
nickels = math.floor(money / 5)
money = money - (5 * nickels)
cents = money
# Add all of the coins in the previous part
coins = quarters + dimes + nickels + cents
# print out the number of coins
print(coins)
