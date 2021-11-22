import random
import logging
import configparser
logging.basicConfig(filename='AŠP.log',encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
config = configparser.ConfigParser()
config.read('./config.ini')


#Izvades teksts, kas uzaicina uz spēli un lūdz uzspiest Enter, lai to sāktu. 
username = input("Welcome to Rock, Paper, Scissors! Enter your name to start: ")
print(username)
#Spēlētāja un datora sākuma punktu skaits.
user_wins = 0
computer_wins = 0

#Iespējamie gājieni
choices = ["rock", "paper", "scissors"]

while True:
#Dators izvēlās vienu no atbildēm.
  random_index = random.randint(0,2)
  cpu_choice = choices[random_index]
#Spēlētājs ievada vienu no atbildēm.
  user_choice = input("Rock, Paper, or Scissors? ").lower()
  while user_choice not in choices:
    user_choice = input("That is not a valid choice. Please try again: ").lower()
  
#Parāda gan datora, gan spēlētāja izvēlēto atbildi.
  print()
  print("Your choice:", user_choice)
  print("Computer's choice:", cpu_choice)
  print()

#Visi iespējamie iznākumi.
  if user_choice == 'rock':
    if cpu_choice == 'rock':
      print("It's a tie!")
    elif cpu_choice == 'scissors':
      print("You win!")
      user_wins+=1
    elif cpu_choice == 'paper':
      print("You lose!")
      computer_wins+=1
  elif user_choice == 'paper':
    if cpu_choice == 'paper':
      print("It's a tie!")
    elif cpu_choice == 'rock':
      print("You win!")
      user_wins+=1
    elif cpu_choice == 'scissors':
      print("You lose!")
      computer_wins+=1
  elif user_choice == 'scissors':
    if cpu_choice == 'scissors':
      print("It's a tie!")
    elif cpu_choice == 'paper':
      print("You win!")
      user_wins+=1
    elif cpu_choice == 'rock':
      print("You lose!")
      computer_wins+=1

#Parāda gan datora, gan spēlētāja uzvaras.
  print()
  print("You have "+str(user_wins)+" wins")
  print("The computer has "+str(computer_wins)+" wins")
  print()
  logging.info("Spēlētāja un datora uzvaras")
#Piedāvā spēlēt vēlreiz. Spiest Y vai N pogu, lai turpinātu spēli vai arī to beigtu.
  repeat = input("Play again? (Y/N) ").lower()
  while repeat not in ['y', 'n']:
    repeat = input("That is not a valid choice. Please try again: ").lower()
  
  if repeat == 'n':
    break

  print("\n----------------------------\n")
