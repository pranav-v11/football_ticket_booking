FOOTBALL MATCH BOOKING APPLICATION

This is an application created using Python (Version - 3.11.5) and MySQL Community Server (Version - 8.0.33)

The purpose of the application is to emulate a website for viewing and booking tickets for football matches with minimal features inside a CLI (Command Line Prompt) while
also using a python library Tkinter to create a GUI which displays the available matches from the sample/working data stored in the respective database

FEATURES:

The application has 7 defined features -

1) ACCOUNT CREATION
   -> user can create an account (without a password) under which all their bookings can be stored
2) LOG IN/ LOG OUT
   -> user can log in to his account by entering the account name(NOT CASE-SENSITIVE) or log out if he is already logged in
3) VIEW MATCHES
   -> user can display all the available matches from the sample/working data stored in the respective MySQL database table
4) VIEW BOOKINGS
   -> user can view all his bookings with relevant data of each booking displayed
5) CANCEL A BOOKING
   -> user can cancel a booking he has made by quoting the booking id to the application
6) DELETE ACCOUNT
   -> user can choose to delete his account and with it all related data like account metadata and bookings made under that account
7) EXIT APPLICATION
   -> user exits the application


PYTHON LIBRARIES USED:

This application uses 3 Python Libraries to perform its functions

1) MYSQL.CONNECTOR 
   -> for connecting to the MySQL database
2) TKINTER
   -> for generating the GUI for displaying matches
3) DATETIME
   -> for handling the date, time and datetime variables imported from the MySQL database table


REQUIRED SCHEMA OBJECTS IN MYSQL:

For the program to run directly with the original code, the following schema objects will need to be created in the MySQL database
(NOTE: Please configure the connection to the database by entering the host, user, password and database name relevant to your system/network)

1) A RUNNING MYSQL DATABASE
   -> enter the name of the database under the database variable in the argument of mysql.connector.connect()


2) A TABLE STORING ACCOUNT DATA 
   -> default name in original code is 'accounts'

   -> run the following command in the MySQL CLI to create the table to be used with default code
      command: create table accounts/<tablename> (AccName varchar(20), AccCreateDate datetime, AccID int PRIMARY KEY AUTO_INCREMENT);

   (NOTE: if you are using a different table name, change the table name in the code as per requirement)


3) A TABLE STORING SAMPLE/WORKING MATCH DATA
   -> contains details of all available matches to choose from

   -> run the following command in the MySQL CLI to create the table to be used with default code
       command: create table fbmatches/<tablename> (LeagueID int, LeagueName varchar(15), HomeTeam varchar(15), AwayTeam varchar(15), MatchDate datetime, MatchVenue varchar(30), 
                TicketPrice_Adult_PrioritySeat int, TicketPrice_Child_PrioritySeat int, TicketPrice_Adult_EconomySeat int, TicketPrice_Child_EconomySeat int, MatchID varchar(20));

   -> There are four ticket types defined in the application, an Adult Priority Seat which is metaphorically the most expensive, followed by the Child Priority Seat, then by the Adult 
       Economy Seat and the least expensive Child Economy Seat

   (NOTE: if you are using a different table name, change the table name in the code as per requirement)

4) A TABLE STORING DATA ON FOOTBALL LEAGUES
   -> contains names of the different football leagues contained in the sample data
   
   -> this application has been exclusively built for 3 football leagues - Premier League, LaLiga and Major League Soccer (MLS)
      (NOTE: if there are more Leagues in your sample/working data, modify the table accordingly and also add more components to the booking_menu() module in the python code as per requirement)
  
   -> run the following command in the MySQL CLI to create the table to be used with default code
      command: create table fbleagues/<tablename> (LeagueID int, LeagueName varchar(15), HostNation varchar(15));

   (NOTE: if you are using a different table name, change the table name in the code as per requirement)

5) A TABLE STORING DATA ON VARIOUS TICKET TYPES
    -> contains names of various ticket types linked to a TicketID
    
    -> run the following command in the MySQL CLI to create the table to be used with default code
       command: create table ticket/<tablename> (TicketID int, TicketName varchar(25))
                insert into ticket/<tablename> values(0, 'Adult(Priority)'),(1,'Child(Priority)'),(2,'Adult(Economy)'),(3,'Child(Economy)');

    (NOTE: if you are using a different table name, change the table name in the code as per requirement)
       
6) A TABLE STORING BOOKING DATA OF ALL USERS
    -> contains booking data of all users
    
    -> run the following command in the MySQL CLI to create the table to be used with default code
       command: create table bookings/<tablename> (AccID int, MatchID varchar(15), BookingDate datetime, TotalAmt int, tickets_bought varchar(200), AccName varchar(25), BookingID int PRIMARY KEY AUTO_INCREMENT);

    (NOTE: if you are using a different table name, change the table name in the code as per requirement)

     


