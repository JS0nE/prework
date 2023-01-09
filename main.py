import math
import stdiomask as maskpass
from time import sleep
import json
import os

def clear():
  os.system('clear')

def pseudo_load(msg):
  full = '. . .'
  while True:
    print(f'{msg}',end="\r")
    sleep(.5)
    print(f'{msg} {full[4:]}',end="\r")
    sleep(.5)
    print(f'{msg} {full[2:]}',end="\r")
    sleep(.5)
    print(f'{msg} {full}', end="\r")
    sleep(.5)
    break

with open('db.json','r') as f:
  global random_accounts
  random_accounts = json.load(f)

def is_intable(value):
  try:
    int(value)
    return True
  except:
    return False

def diagnostic_print(*toprint):
  term_size = os.get_terminal_size()
  print('=' * term_size.columns)
  print(toprint)

def getAccount(cc,pin,ssn_short):
  if (len(cc)==16,len(pin)==4,len(ssn_short)==4):
    if (is_intable(cc),is_intable(pin),is_intable(ssn_short)):

      for i in random_accounts:
        db_cc = str(random_accounts[i]['Credentials']['CC'])
        db_pin = str(random_accounts[i]['Credentials']['PIN'])
        db_ssn = str(random_accounts[i]['Credentials']['SSN'])[5:]

        if cc == db_cc and pin == db_pin and ssn_short == db_ssn:
          return [True, random_accounts[i]]

      return[False, 'account not found']

  else:
    return [False, 'CC# must be 16 digits, PIN must be 4 digits, the last 4 digits of your SSN must be 4 digits']


def getCredentials():
  clear()
  print("Sure, but I  do need some information from you before we begin.")
  sleep(1)
  CC = maskpass.getpass(prompt="\nPlease type your full Credit/Debit card number:\n", mask="*")
  sleep(1)
  PIN = maskpass.getpass(prompt="\nGreat!, now please type your Personal Identification Number (PIN):\n", mask="*")
  sleep(1)
  SSN_SHORT = maskpass.getpass(prompt="\nAnd one last time, please type in the last four digits of your Social Security Number (SSN):\n", mask="*")
  clear()
  return (CC,PIN,SSN_SHORT)


def checkBal():
  
  while True:
    credentials = getCredentials()
    pseudo_load('Please wait')

    result = getAccount(credentials[0],credentials[1],credentials[2])
    if result[0] == False:
      print(f'\nSorry, {result[1]}.')
      sleep(1)
      break
    elif result[0] == True:
      name = result[1]['Credentials']['Name']
      bal = result[1]['Checking']['Balance']
      print("\n")
      print(f"Welcome {name}. Your 'Checking' has a balance of {bal}")
      sleep(1)
      break

def returnRecentPurchases():
  while True:
    credentials = getCredentials()
    account = getAccount(credentials[0],credentials[1],credentials[2])
    pseudo_load('Please wait')

    if account[0]:
      purchase_log = account[1]['Checking']['Purchase_Log']
      clear()
      print(f"Hello {account[1]['Credentials']['Name']}. Here are your recent purchases.")
      if len(purchase_log.keys()) <= 3:
        li = list(purchase_log.keys())
        for i in purchase_log:
          count = 1
          dict_item = purchase_log[i]
          vendor = dict_item['Vendor']
          item = dict_item['Item']
          cost = dict_item['Cost']

          print(f"\nItem{count}\n  Vender:{vendor}\n  Item:{item}\n  Cost:{cost}")
          count=count+1
          

      elif len(purchase_log.keys()) > 3:
        li = list(purchase_log.keys())
        for i in range(0,2):
          i_name = li[i]
          dict_item = purchase_log[i_name]
          vendor = dict_item['Vendor']
          item = dict_item['Item']
          cost = dict_item['Cost']
          print(f"\nItem{i+1}\n  Vender:{vendor}\n  Item:{item}\n  Cost:{cost}")
      break
    elif not account[0]:
      print(f'Sorry, {account[1]}')
      break



responses = {
  'balance': checkBal,
  'purchases': returnRecentPurchases
}

response = input('What can I help you with today?\n')
running = True

def exec():
  for i in responses.keys():
    if i in response:
      responses[i]()
      return
  print("Sorry, I can't help you with that.")
  sleep(.5)

while running:
  if 'end' in response:
      print('\nNo problem! Thank you for choosing Imaginary Bank.')
      break
  exec()
  response = input('\nAnything else I can help you with?\n')