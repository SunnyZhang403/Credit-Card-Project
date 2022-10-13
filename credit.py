def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global accountstatus

    accountstatus = "active" #default status is active

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = 0, 0

    last_country = None
    last_country2 = None


def updateacc(day, month):
    global cur_balance_owing_recent, cur_balance_owing_intst, last_update_month, last_update_day

    if month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_intst * 1.05
        cur_balance_owing_intst = cur_balance_owing_intst + cur_balance_owing_recent
        cur_balance_owing_intst = cur_balance_owing_intst*(1.05**(month-last_update_month-1))
        cur_balance_owing_recent = 0
    # else:
    #     last_update_month = month
    #     last_update_day = day
    last_update_day = day
    last_update_month = month





def date_same_or_later(day1, month1, day2, month2):
    if month1 == month2 and day1 >= day2:
        return True
    elif month1 > month2:
        return True
    else:
        return False


def all_three_different(c1, c2, c3):
    if c1 == c2 or c2 == c3 or c1 == c3:
        return False
    else:
        return True

def disableaccount():
    global accountstatus
    accountstatus = "disabled"

def purchase(amount, day, month, country):
    global cur_balance_owing_recent, last_country, last_country2, last_update_day, last_update_month, accountstatus
    if date_same_or_later(day, month, last_update_day, last_update_month) == True and all_three_different(last_country, last_country2, country)== False and accountstatus == "active":

        updateacc(day, month)
        last_country2 = last_country
        last_country = country
        cur_balance_owing_recent = cur_balance_owing_recent + amount
    else:
        disableaccount()
        return "error"
def amount_owed(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    updateacc(day, month)
    return cur_balance_owing_recent + cur_balance_owing_intst


def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent

    if accountstatus == "disabled" or date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    updateacc(day, month)
    if amount > cur_balance_owing_intst:

        cur_balance_owing_recent = cur_balance_owing_recent - (amount - cur_balance_owing_intst)

        cur_balance_owing_intst = 0

    else:
        cur_balance_owing_intst = cur_balance_owing_intst - amount



# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':

    initialize()
    print("Current balance is:", amount_owed(1, 1)) #verify that starting balance is correct and initialized properly - 0.0
    purchase(20, 2, 1, "Canada")
    print("Current balance is:", amount_owed(2, 1)) #verify first purchase went through properly - 20.0
    print("Current balance is:", amount_owed(2, 2)) #verify that no interest is paid on this payment (interest should be charged on the
                                                    #balance accruing interest prior to the monthly balance being transferred) - 20.0
    pay_bill(10, 3, 2)
    print("Current balance is:", amount_owed(3, 2)) #verify bill was paid - 10
    print("Current balance is:", amount_owed(3, 3)) #verify interest charged on remaining money - 10.5
    purchase(50, 4, 3, "Canada")
    pay_bill(55, 5, 3) #verify the bill paying works even if the amount paid > the amount accruing interest
    print("Current balance is:", amount_owed(6, 3)) #5.5
    pay_bill(5.5, 6, 3) #clear account for convenience
    purchase(100, 6, 3, "Canada")
    print("Current balance is:", amount_owed(6, 6)) #test interest for several months - 110.25
    purchase(1,7,6, "United States")
    purchase(1,8,6, "Mexico") #test disabling
    print("Current balance is:", amount_owed(9, 6)) #111.25 (only adds the United States transaction but not the Mexico transaction)
    purchase(1, 9, 6, "Canada") #error
    accountstatus = "active" #re-enable account for further testing

    purchase(1,8,6,"Canada") #error
    print("Current balance is:", amount_owed(8,6))

