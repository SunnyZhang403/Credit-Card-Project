
# You should modify initialize()
def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global accountstatus

    accountstatus = "active" #dfault status is active

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = 0, 0

    last_country = None
    last_country2 = None

    MONTHLY_INTEREST_RATE = 0.05

def updateacc(day, month):
    global cur_balance_owing_recent, cur_balance_owing_intst, last_update_month, last_update_day

    if month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_intst * 1.05
        cur_balance_owing_intst = cur_balance_owing_intst + cur_balance_owing_recent
        cur_balance_owing_intst = cur_balance_owing_intst*(1.05**(month-last_update_month-1))
        cur_balance_owing_recent = 0
    else:
        last_update_month = month
        last_update_day = day
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
    if c1 == c2 or c2 == c3 or c1 ==c3:
        return False
    else:
        return True

def disableaccount():
    global accountstatus
    accountstatus = "disabled"

def purchase(amount, day, month, country):
    global cur_balance_owing_recent, last_country, last_country2, last_update_day, last_update_month, accountstatus
    if date_same_or_later(day, month, last_update_day, last_update_month) == True and all_three_different(last_country,last_country2,country)== False and accountstatus == "active":

        updateacc(day, month)
        last_country2 = last_country
        last_country = country
        cur_balance_owing_recent = cur_balance_owing_recent + amount
    else:
        disableaccount()
        # print("Account is disabled")
        return "error"
def amount_owed(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    updateacc(day, month)
    return cur_balance_owing_recent + cur_balance_owing_intst


def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent

    if accountstatus == "disabled":
        # print("Account is disabled")
        return "error"
    updateacc(day,month)
    if amount > cur_balance_owing_intst:
        cur_balance_owing_intst = 0
        cur_balance_owing_recent = cur_balance_owing_recent - (amount - cur_balance_owing_intst)
    else:
        cur_balance_owing_intst = cur_balance_owing_intst - amount



# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0                              (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                 (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)               (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)               (Test4)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)               (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05) (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                          (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in    (Test8)
                                                #          a row)
    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase     (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)          (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                        (Test11)
                                                # (43.65375*1.05+40)

