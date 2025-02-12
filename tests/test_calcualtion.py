import pytest
from app.calcualtion import add , substract , devision , mode , multiply , BankAccount


@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1,num2,expected",[(3,2,5),(7,3,10),(10,10,20)])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected
def test_sub():
    assert substract(10,5) == 5
def test_multy():
    assert multiply(4,5) == 20
def test_devsion():
    assert devision(10,2) == 5 
def test_mod():
    assert mode(10,2) == 0


def test_bank_set_initial_Amount(bank_account):
    # bank_account = BankAccount(50) 
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    # bannk_account = BankAccount()
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw_amount(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(23)
    assert bank_account.balance == 27


def test_deposit(bank_account):
    # bank_account = BankAccount(120)
    bank_account.deposit(60)
    assert bank_account.balance == 110


def test_collect_intrest():
    bank_account =BankAccount(50)
    bank_account.collect_interest()
    assert bank_account.balance == 55.00000000000001


@pytest.mark.parametrize("deposited,withdraw,expected",[(200,100,100),(50,20,30),(10000,9000,1000),(100,50,50)])
def test_bank_transaction(zero_bank_account,deposited,withdraw,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

# def test_insufficient_fund(bank_account):
#     with pytest.raises(Exception):
#         bank_account.withdraw(0)    







    


    


