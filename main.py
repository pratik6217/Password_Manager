import pymongo
import getpass
import random
import string
import pyperclip
from cryptography.fernet import Fernet
import smtplib, ssl

#key = Fernet.generate_key() #Only execute this once.
'''with open("key.key", "w") as file:
  file.write(key.decode())'''

with open("key.key", "r") as file:
  key = file.read()


f = Fernet(key)

def send_mail(mail):
  context = ssl.create_default_context()
  port = 465
  email = "passvault6217@gmail.com"
  with open("password.key", "r") as f:
    password = f.read()
  message = """\
Subject: Registration Succesfull.

This message is to inform you that you have successfully registered with our services.

Thankyou for choosing us :)"""
  receiver = mail
  try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context = context)
    server.ehlo()
    #server.starttls(context = context)
    server.login(email, password)
    server.ehlo()
    server.sendmail(email, receiver, message)
  except Exception as e:
    print(e)
  finally:
    server.quit()
  return


def login():
  print("Login:\n")
  flag = False
  while True:
    u_name = input("Please enter your username:\n")
    print("Please enter your password:")
    password = getpass.getpass()
    encrypted_password = f.encrypt(password.encode())
    data = records.find_one({"name" : u_name})
    if data:
      if f.decrypt(data['password']).decode() == password:
        print("Welcome to your dashboard,",u_name)
        flag = True
        break
      else:
        print("Please enter correct details !!")
        continue
    else:
      print("Please enter correct details !!")
      continue
    
  pointer = db[u_name]
  print()
  ch = int(input('''Please select an option:
  1.Enter Credentials.
  2.Update Credentials.
  3.Delete Credentials.
  4.View Credentials.
  5.View For an Organiation.\n\n'''))

  if ch == 1:
    web = input("\nPlease enter the website:\n")
    print("Please enter your password:")
    password = getpass.getpass()
    d = {"Organization" : web,
           "password" : f.encrypt(password.encode())
    }
    succ = pointer.insert_one(d)
    if succ:
      print("Your Credentials were added successfully.")
    else:
      print("There was a problem !!")

  elif ch == 2:
    org = input("Enter the Organizations name to update details for it:\n")
    document = pointer.find_one({"Organization" : org})
    if document:
      print("Please enter the Details you want to update:\n1.Organization.\n2.Password")
      select = int(input())
      if select == 1:
        new_value = input("Enter the New Value:\n")
        old_value = {"Organization" : org}
        update_value = {"$set" : {"Organization" : new_value}}
        try:
          pointer.update_one(old_value, update_value)
        except Exception as e:
          print(e)
      elif select == 2:
        old_pass = f.decrypt(document["password"]).decode()
        print("Enter the new Password:\n")
        new_pass = getpass.getpass()
        old = {"password" : document['password']}
        new = {"$set" : {"password" : f.encrypt(new_pass.encode())}}
        try:
          pointer.update_one(old, new)
        except Exception as e:
          print(e)

  elif ch == 3:
    print("Please Choose one:\n1.Delete an Entry.\n2.Delete all entries.")
    select = int(input())
    if select == 1:
      org = input("Enter the Organization's name:\n ")
      result = pointer.delete_one({"Organization" : org})
      if result:
        print("Deleted Succesfully !!")
      else:
        print("Some Error Occured !! Try Again.")

    elif select == 2:
      result = pointer.delete({})
      if result:
        print("Deleted all the entries")
      else:
        print('Some Error Occured !! Try Again.')

  elif ch == 4:
    cursor = pointer.find({})
    for document in cursor:
      print()
      print("Organization :", document["Organization"])
      print("Password :", f.decrypt(document["password"]).decode())
        
  elif ch ==5:
    org = input("\nEnter the Organization's name or Website:\n")
    document = pointer.find_one({"Organization" : org})
    if result:
      print()
      print("Organization :", document["Organization"])
      print("Password :", f.decrypt(document["password"]).decode())
    else:
      print("No such Entry Exists !!")
  

try:
  client = pymongo.MongoClient("mongodb+srv://admin:admin@password-manager.bl1uj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
  db = client["Password_manager"]
  records = db["Login"]
except:
  print("Cannot Connect to the Database !!")

print("".rjust(30) + "* " * 30 )
for i in range(10):
  print("".rjust(30) + "*" + "  " * 28 + " *")
  if i == 1:
    print("".rjust(30) +"*" + " ".rjust(22) + "Password Manager" + " ".rjust(19) + "*")
  if i == 3:
    print("".rjust(31)  + "* " * 28 + " *")
  if i == 5:
    print("".rjust(30) +"*" + " ".rjust(22) + "Created By:" + " ".rjust(24) + "*")
    print("".rjust(30)  + "*" + "  " * 28 + " *")
    print("".rjust(30) +"*" + " ".rjust(22) + "Pratik Mishra" + " ".rjust(22) + "*")
print("".rjust(30) + "* " * 30)

print()
print()
while True:
  op = int(input('''Welcome to our Password-Manager

  Please select an option to continue:
  1. Register.
  2. Login.
  3. Generate a random Password.
  4. Exit.

  '''))

  if op == 1:
    while True:
      email = input("Enter you Gmail-Id:\n")
      u_name = input("Please enter a username:\n")
      if records.find_one({"name" : u_name}):
        print("This username is not available or already taken by someone !!")
        continue
      else:
        break
    print("Please enter your password:")
    password = getpass.getpass()
    password = f.encrypt(password.encode())
    new_user = {
        'name' : u_name,
        'password' : password
    }

    succ = records.insert_one(new_user)
    if succ:
      print("Succesfully Registered !")
      send_mail(email)
      print()
    
      

  elif op == 2:
    login()
    break
    
    
  elif op == 3:
      while True:
        password = ""
        pass_option = input("Please select an option:\n1.Mixed - Upper, Lower, Digits(Most Secure).\n2.Lowercase.\n3.Uppercase.\n")
        if pass_option == "1":
          print()
          length = input("Please enter the length of the password you want to generate(For a strong Password go for length >= 8):\n")
          print()
          for i in range(int(length)):
            password += random.choice([random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits)])
          
        elif pass_option == "2":
          length = input("Please enter the length of the password you want to generate:\n")
          print()
          for i in range(int(length)):
            password += random.choice([random.choice(string.ascii_lowercase)])

        elif pass_option == "3":
          length = input("Please enter the length of the password you want to generate:\n")
          print()
          for i in range(int(length)):
            password += random.choice([random.choice(string.ascii_uppercase)])
            
        print(password)
        print()
        final_option = input("Please select an option:\n1.copy the password to the clipboard and exit.\n2.Regenerate?\n3.Exit.\n")
        if final_option == "1":
          pyperclip.copy(password)
          print("Your newly generated password has been copied to the clipboard.")
          break
        elif final_option == "2":
          continue
        else:
          print()
          print("Thankyou :)\nHave a nice day !!")
          print()
          break
  elif op == 4:
    print('Thankyou for Using our service.')
    break


