import random
import logging
import configparser
import mysql.connector
import os

os.chdir(os.path.dirname(__file__))

from mysql.connector import Error

logging.basicConfig(filename='ASP.log',encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
config = configparser.ConfigParser()
config.read('./config.ini')

logger = logging.getLogger('root')

logger.info('Processing mysql config file')

mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')

connection = None
connected = False

def init_db():
	global connection
	connection = mysql.connector.connect(host = mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)

init_db()

def get_cursor():
	global connection
	try:
		connection.ping(reconnect=True, attempts=1, delay=0)
		connection.commit()
	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))
		connection = init_db()
		connection.commit()
	return connection.cursor()

#Ievadītās vērtības tiks pievienotas datubāzei
def mysql_insert_result_into_db(username, user_wins, computer_wins):
	cursor = get_cursor()
	try:
		cursor = connection.cursor()
		result  = cursor.execute( "INSERT INTO `asp` (`Name`, `Wins`, `Loses`) VALUES ('" + str(username) + "', '" + str(user_wins) + "', '" + str(computer_wins) + "') ")
		connection.commit()
	except Error as e :
		logger.error( "INSERT INTO `asp` (`Name`, `Wins`, `Loses`) VALUES ('" + str(username) + "', '" + str(user_wins) + "', '" + str(computer_wins) + "') " )
		logger.error('Problem inserting game values into DB: ' + str(e))
		pass

#Izvades teksts, kas uzaicina uz spēli un lūdz ievadīt vārdu, lai to sāktu..
username = input("Welcome to Rock, Paper, Scissors! Enter your name to start: ")

#Spēlētāja un datora sākuma punktu skaits.
user_wins = 0
computer_wins = 0

#Iespējamie gājieni
choices = ["rock", "paper", "scissors"]

while True:
#Dators izvēlās vienu no atbildēm.
  random_index = random.randint(0,2)
  cpu_choice = choices[random_index]
  logging.info("CPU choice")
#Spēlētājs ievada vienu no atbildēm.
  user_choice = input("Rock, Paper, or Scissors? ").lower()
  while user_choice not in choices:
    user_choice = input("That is not a valid choice. Please try again: ").lower()
  logging.info("User choice")
#Parāda gan datora, gan spēlētāja izvēlēto atbildi.
  print()
  print("Your choice:", user_choice)
  print("Computer's choice:", cpu_choice)
  print()
  logging.info("Shows both choices")
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
  logging.info("Spēlētāja uzvaras " + str(user_wins) + " un datora uzvaras " + str(computer_wins))
#Piedāvā spēlēt vēlreiz. Spiest Y vai N pogu, lai turpinātu spēli vai arī to beigtu.
  repeat = input("Play again? (Y/N) ").lower()
  while repeat not in ['y', 'n']:
    repeat = input("That is not a valid choice. Please try again: ").lower()
    logging.info("Continue playing or end playing")
  if repeat == 'n':
    mysql_insert_result_into_db(username, user_wins, computer_wins)
    break

  print("\n----------------------------\n")
