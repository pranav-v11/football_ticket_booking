#importing and initialising libraries------------------------------------------------------------------------------------------------
import tkinter 
from tkinter import ttk 
from tkinter import *
import mysql.connector
import datetime 


mycon = mysql.connector.connect(host="<hostname>", user="<username>", password="<password>", database="<databasename>", auth_plugin = "mysql_native_password")
cs = mycon.cursor(buffered=True)
r = tkinter.Tk() 
leaguetitle = "All"
headername = 'Selected Matches ('+leaguetitle+')'
status = 1
loggedin = ""



#defining all components/modules of program -----------------------------------------------------------------------------------------



#login/logout module------------------------------------------------------------------------------------------------------------------
def login_logout_module():
 while True:
    global status
    global loggedin


    if status == 0:
        print('''You are currently logged in
            would you like to logout of your account? (y/n)''')
        choice1 = input("Enter yes(y) or no(n): ")
        if choice1.lower() == "y":
            status = 1
            loggedin = ""
            print("You have been logged out of your account")
            choice1 = ""
            break
        elif choice1.lower() == "n":
            choice1 = ""
            break
        else:
            print("Please enter a valid command and try again")
            choice1 = ""
            continue
    elif status == 1:
        print('''You aren't currently logged into any account 
              would you like to log in? (y/n)''')
        choice1 = input("Enter yes(y) or no(n): ")
        if choice1.lower() == "y":
            print ("Please enter the login credentials: ")
            userinput = input("Enter username: ")
            query1 = "SELECT AccName FROM accounts"
            cs.execute(query1)
            data1 = cs.fetchall()
            idk2 = []
            for row in data1:
                app = row[0]
                idk2.append(app)
            if userinput.lower() in idk2 :
                status = 0
                loggedin = userinput.lower()
                print("You have logged in to your account")
                break
            else:
                print('''This username is not linked to any registered account
                      Please use the create account menu to create a new account
                      or check for any mistakes in the username entered ''')
                break
        elif choice1 =="n":
            break
        else:
            print("Please enter a valid command and try again")
            choice1 = ""
            continue   
    else:
        print("An error has occured in the program: INVALID STATUS VARIABLE VALUE")
        break


#accountcreation module---------------------------------------------------------------------------------------------------------------
def accountcrt():
    while True:
        global status
        global loggedin  

        if status == 0:
            print("You are already logged into an account, please logout first")
            break
        
        elif status==1:
            choice2 = input("Are you sure you want to create a new account? [Enter yes(y)/no(n) ]: ")
            if choice2.lower() == "n":
                break
            elif choice2.lower() == "y":
                accNameINPUT = input("Please enter the name of the account you wish to create (Max Char Limit - 20) ")
                if len(accNameINPUT) > 20:
                    print("Name exceeds allowed character length, please try again")
                    continue
                else:
                  query2 = "SELECT AccName FROM accounts"
                  cs.execute(query2)
                  data2 = cs.fetchall()
                  idk1 = []
                  for row in data2:
                   app = row[0]
                   idk1.append(app)
                  if accNameINPUT.lower() in idk1:
                      print("There is already an account with this name, please enter a new account name which is unique")
                      continue 
                  elif accNameINPUT.lower() not in idk1:
                      acccrtquery = "INSERT INTO accounts(AccName, AccCreateDate) values(%s, sysdate())"
                      values = (accNameINPUT.lower(),)
                      cs.execute(acccrtquery, values)
                      mycon.commit()
                      print("Your account has successfuly been created")
                      status = 0
                      loggedin = accNameINPUT.lower()
                      print("You have now been logged in to your newly created account")
                      break
            else: 
                print("Please enter a valid command and try again")
                choice2 = ""
                continue
        else:
            print("An error has occured in the program: INVALID STATUS VARIABLE VALUE")
            break
      
        
#module which places booking and updates database as per requirement------------------------------------------------------------------
def place_booking():
     e = True
     while e == True:

          print('''Please enter the following details to place your booking''')
          matchidentifier = input("Please enter the unique ID of the match you want to book (refer to Match ID column)")
          cs.execute("SELECT MatchID FROM fbmatches")
          databook = cs.fetchall()
          databookex = []
          for row in databook:
            databookex.append(row[0])


          if matchidentifier not in databookex:
              print("Invalid MatchID entered, enter a valid MatchID and try again")
              continue
          elif matchidentifier in databookex:
              tickpricequery=("SELECT TicketPrice_Adult_PrioritySeat, TicketPrice_Child_PrioritySeat, TicketPrice_Adult_EconomySeat, TicketPrice_Child_EconomySeat FROM fbmatches WHERE MatchID = %s")
              cs.execute(tickpricequery, (matchidentifier,))
              datatickets = cs.fetchall()
              dataticketsex = []
              for row in datatickets:
                 dataticketsex.append(row[0])
                 dataticketsex.append(row[1])
                 dataticketsex.append(row[2])
                 dataticketsex.append(row[3])
              more = True
              purchaseddict = {'Adult(Priority)':0, 'Child(Priority)':0, 'Adult(Economy)':0, 'Child(Economy)':0}
              multpertick = {}
              no = 0
              dictcheck = {'Adult(Priority)':0, 'Child(Priority)':0, 'Adult(Economy)':0, 'Child(Economy)':0}


              while more == True:  
                  print (''' Please select the ticket type:
                         Adult (Priority) [type 0] : ''',dataticketsex[0],
                         ''' 
                         Child (Priority) [type 1] : ''',dataticketsex[1],
                          '''
                         Adult (Economy)  [type 2] : ''', dataticketsex[2],
                         '''
                         Child (Economy)  [type 3] : ''', dataticketsex[3] )
                  
                  tick = input("Enter your choice: ")

                  if tick not in ('0', '1', '2', '3'):
                      print("Please enter a valid command and try again")
                      continue
                  else:
                      tickselecquery = "SELECT TicketName FROM ticket WHERE TicketID =%s"
                      cs.execute(tickselecquery,(int(tick),))
                      datatickextra = cs.fetchall()
                      datatickex = []
                      for row in datatickextra:
                         datatickex.append(row[0])
                      tickname = datatickex[0]
                      multiplier = int(input("How many such tickets do you need? (max 10 per category per booking)"))
                      y = dictcheck.get(tickname)
                      multpertick[tickname] = y + multiplier
                      no = multpertick.get(tickname)
                      dictcheck[tickname] = no
                      no = 0
                      x = dictcheck.get(tickname)
                      if  x>10 or  x<1:
                          print("You have exceeded the ticket amount limit/Entered an invalid ticket amount, please try again")
                          if y == 0:
                             multpertick[tickname] = 0
                             dictcheck[tickname]=0
                             continue 
                          else:
                             multpertick[tickname] = 0
                             dictcheck[tickname]=y 
                      elif x<=10 and x>=1:
                        multpertick[tickname]=0
                        while True:  
                            totalprice = dataticketsex[int(tick)]*multiplier
                            intchoice4 = input("Do you want to purchase more tickets? (y/n)")
                            if intchoice4.lower() == "n":
                               z = purchaseddict.get(tickname)
                               purchaseddict[tickname] = z + totalprice
                               multiplier = 0
                               more = False
                               break
                            elif intchoice4.lower() =="y":
                               if purchaseddict.get(tickname) == None:
                                  purchaseddict[tickname] = totalprice
                               else:
                                  z = purchaseddict.get(tickname)
                                  purchaseddict[tickname] = z + totalprice
                               
                               
                               multiplier = 0
                               more = True
                               break 
                            else:
                               print("Please enter a valid command and try again")
                               multiplier = 0
                               more = True 
                               continue
              print('Your booking summary for Match ID: ',matchidentifier,' is: ')
              randquery1 = "SELECT HomeTeam, AwayTeam, MatchDate, MatchVenue FROM fbmatches WHERE MatchID = %s"
              cs.execute(randquery1, (matchidentifier,))
              randdata1 = cs.fetchall()
              randdata1ex = []
              for row in randdata1:
                 randdata1ex.append(row[0])
                 randdata1ex.append(row[1])
                 randdata1ex.append(row[2])
                 randdata1ex.append(row[3])
    
              hometeam = randdata1ex[0]
              awayteam = randdata1ex[1]
              matchdate = randdata1ex[2]
              venue = randdata1ex[3]  
              print('''MATCH ID: ''',matchidentifier,
                    '''HOME TEAM: ''',hometeam,
                    '''AWAY TEAM: ''',awayteam,
                    '''DATE: ''',matchdate,
                    '''VENUE/STADIUM: ''',venue)
              print(dictcheck)
              print('''BOOKED TICKETS
                    Adult-Priority: x''',dictcheck['Adult(Priority)'],''' for ''',purchaseddict['Adult(Priority)'],'''$

                    Child-Priority: x''',dictcheck['Child(Priority)'],''' for ''',purchaseddict['Child(Priority)'],'''$

                    Adult-Economy: x''',dictcheck['Adult(Economy)'],''' for ''',purchaseddict['Adult(Economy)'],'''$

                    Child-Economy: x''',dictcheck['Child(Economy)'],''' for ''',purchaseddict['Child(Economy)'],'''$''')
              print('''TOTAL PRICE: ''',purchaseddict['Adult(Priority)'] + purchaseddict['Child(Priority)'] + purchaseddict['Adult(Economy)'] + purchaseddict['Child(Economy)'],'$')
              print("Adding booking to your booking history")  
              keyslist = list(dictcheck.keys())
              insertpurchdict = '{"'+keyslist[0]+'": '+str(dictcheck.get(keyslist[0]))+', "'+keyslist[1]+'": '+str(dictcheck.get(keyslist[1]))+', "'+keyslist[2]+'": '+str(dictcheck.get(keyslist[2]))+', "'+keyslist[3]+'": '+str(dictcheck.get(keyslist[3]))+'}'
              bookinginsertquery = "INSERT INTO bookings (AccName, AccID, MatchID, BookingDate, TotalAmt, tickets_bought) VALUES(%s, %s, %s, sysdate(), %s, %s)"
              cs.execute(bookinginsertquery,(loggedin, accid, matchidentifier, purchaseddict['Adult(Priority)'] + purchaseddict['Child(Priority)'] + purchaseddict['Adult(Economy)'] + purchaseddict['Child(Economy)'], insertpurchdict,))
              mycon.commit()
              print("Your booking has successfuly been completed")
              while True:
                  
                ask = input('Do you want to make another booking? (y/n): ')
                if ask == "n":
                   e = False
                   break  
                elif ask == "y":
                   e = True
                   break
                else: 
                   print("Please enter a valid command and try again ")
                   continue 

#module to initialise variables and create menu for starting a booking and also show matches------------------------------------------
def booking_menu():
  global status
  global loggedin
  global leaguetitle
  global accid
  global headername
  accid = "N.A"
  while True:
    
    
    if status == 1:
        print("You are currently not logged in, please login and try again")
        break
    elif status == 0:
      openingquery = 'SELECT AccID FROM accounts WHERE AccName = %s'
      cs.execute(openingquery, (loggedin,))
      opendata = cs.fetchall()
      accid = int(opendata[0][0])
      print("Welcome to the Ticket Booking Portal")
      choice3 = input("Would you like to view and book matches? [Enter yes(y)/no(n) ] : ")
      if choice3.lower() == "n":
         break
      elif choice3.lower() == "y":
         print('''There are three leagues to choose from
             (League ID)  (League Name)              (Host Country)
              1             Premier League             England
              2             LaLiga                     Spain
              3             Major League Soccer (MLS)  United States''')
         print('''Please enter the LeagueID of the League whose matches you would like to view
             OR ENTER '0' to view matches accross ALL LEAGUES''')
         intchoice3 = int(input("Enter your choice: "))
         if intchoice3 == 0:
            leaguetitle = "All"

            print("Displaying all available matches in popup")
            r.title(headername)
            r.geometry("1280x720")
            cs.execute("SELECT MatchID, LeagueName, HomeTeam, AwayTeam, MatchDate, MatchVenue FROM fbmatches")
            tree = ttk.Treeview(r, selectmode='browse',height=35)
            tree['show']='headings' 
            s = ttk.Style(r)
            s.theme_use("clam")
            tree["columns"] = ("MatchID", "LeagueName", "HomeTeam", "AwayTeam", "MatchDate", "MatchVenue" )
            tree.column("MatchID", width=100, minwidth=100, anchor = tkinter.CENTER)
            tree.column("LeagueName", width=150, minwidth=150, anchor = tkinter.CENTER)
            tree.column("HomeTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
            tree.column("AwayTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
            tree.column("MatchDate", width=150, minwidth=150, anchor = tkinter.CENTER)
            tree.column("MatchVenue", width=400, minwidth=400, anchor = tkinter.CENTER)

            tree.heading("MatchID", text="Match ID", anchor = tkinter.CENTER)
            tree.heading("LeagueName", text="League Name", anchor = tkinter.CENTER)
            tree.heading("HomeTeam", text="Home Team", anchor = tkinter.CENTER)
            tree.heading("AwayTeam", text="Away Team", anchor = tkinter.CENTER)
            tree.heading("MatchDate", text="Date", anchor = tkinter.CENTER)
            tree.heading("MatchVenue", text="Venue/Stadium", anchor = tkinter.CENTER)

            i = 0
            for row in cs:
                tree.insert('', i,  text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                i = i+1
            vs = ttk.Scrollbar(r,orient="vertical")
            vs.configure(command=tree.yview)
            tree.configure(yscrollcommand=vs.set)
            vs.pack(fill="y",side="right")
            hsb = ttk.Scrollbar(r,orient='horizontal')
            hsb.configure(command=tree.xview)
            tree.configure(xscrollcommand=hsb.set)
            hsb.pack(fill="x",side="bottom")
            tree.pack()
            place_booking()
            break
            r.mainloop()

         elif intchoice3 == 1:
          leaguetitle = 'Premier League'

          print("Displaying all available Premier League matches in popup")
          r.title(headername)
          r.geometry("1280x720")
          cs.execute("SELECT MatchID, LeagueName, HomeTeam, AwayTeam, MatchDate, MatchVenue FROM fbmatches WHERE LeagueID = 1")
          tree = ttk.Treeview(r, selectmode='browse',height=10)
          tree['show']='headings'
          s = ttk.Style(r)
          s.theme_use("clam") 
          tree["columns"] = ("MatchID", "LeagueName", "HomeTeam", "AwayTeam", "MatchDate", "MatchVenue" )
          tree.column("MatchID", width=100, minwidth=100, anchor = tkinter.CENTER)
          tree.column("LeagueName", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("HomeTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("AwayTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchDate", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchVenue", width=400, minwidth=400, anchor = tkinter.CENTER)
          
          tree.heading("MatchID", text="Match ID", anchor = tkinter.CENTER)
          tree.heading("LeagueName", text="League Name", anchor = tkinter.CENTER)
          tree.heading("HomeTeam", text="Home Team", anchor = tkinter.CENTER)
          tree.heading("AwayTeam", text="Away Team", anchor = tkinter.CENTER)
          tree.heading("MatchDate", text="Date", anchor = tkinter.CENTER)
          tree.heading("MatchVenue", text="Venue/Stadium", anchor = tkinter.CENTER)

          i = 0
          for row in cs:
                tree.insert('', i,  text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                i = i+1
          vs = ttk.Scrollbar(r,orient="vertical")
          vs.configure(command=tree.yview)
          tree.configure(yscrollcommand=vs.set)
          vs.pack(fill="y",side="right")
          hsb = ttk.Scrollbar(r,orient='horizontal')
          hsb.configure(command=tree.xview)
          tree.configure(xscrollcommand=hsb.set)
          hsb.pack(fill="x",side="bottom")
          tree.pack()
          place_booking()
          break
          r.mainloop()

         elif intchoice3 == 2:
          leaguetitle = 'LaLiga'

          print("Displaying all available LaLiga matches in popup")
          r.title(headername)
          r.geometry("1280x720")
          cs.execute("SELECT MatchID, LeagueName, HomeTeam, AwayTeam, MatchDate, MatchVenue FROM fbmatches WHERE LeagueID = 2")
          tree = ttk.Treeview(r, selectmode='browse',height=10)
          tree['show']='headings' 
          s = ttk.Style(r)
          s.theme_use("clam") 
          tree["columns"] = ("MatchID", "LeagueName", "HomeTeam", "AwayTeam", "MatchDate", "MatchVenue" )
          tree.column("MatchID", width=100, minwidth=100, anchor = tkinter.CENTER)
          tree.column("LeagueName", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("HomeTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("AwayTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchDate", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchVenue", width=400, minwidth=400, anchor = tkinter.CENTER)

          tree.heading("MatchID", text="Match ID", anchor = tkinter.CENTER)
          tree.heading("LeagueName", text="League Name", anchor = tkinter.CENTER)
          tree.heading("HomeTeam", text="Home Team", anchor = tkinter.CENTER)
          tree.heading("AwayTeam", text="Away Team", anchor = tkinter.CENTER)
          tree.heading("MatchDate", text="Date", anchor = tkinter.CENTER)
          tree.heading("MatchVenue", text="Venue/Stadium", anchor = tkinter.CENTER)
          
          i=0
          for row in cs:
              tree.insert('', i, text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]) )
              i = i+1
          vs = ttk.Scrollbar(r,orient="vertical")
          vs.configure(command=tree.yview)
          tree.configure(yscrollcommand=vs.set)
          vs.pack(fill="y",side="right")
          hsb = ttk.Scrollbar(r,orient='horizontal')
          hsb.configure(command=tree.xview)
          tree.configure(xscrollcommand=hsb.set)
          hsb.pack(fill="x",side="bottom")
          tree.pack()
          place_booking()
          break
          r.mainloop()
        
         elif intchoice3 == 3:
          leaguetitle = 'Major League Soccer'

          print("Displaying all available Lajor League Soccer(MLS) matches in popup")
          r.title(headername)
          r.geometry("1280x720")
          cs.execute("SELECT MatchID, LeagueName, HomeTeam, AwayTeam, MatchDate, MatchVenue FROM fbmatches WHERE LeagueID = 3")
          tree = ttk.Treeview(r, selectmode='browse',height=15)
          tree['show']='headings' 
          s = ttk.Style(r)
          s.theme_use("clam") 
          tree["columns"] = ("MatchID", "LeagueName", "HomeTeam", "AwayTeam", "MatchDate", "MatchVenue" )
          tree.column("MatchID", width=100, minwidth=100, anchor = tkinter.CENTER)
          tree.column("LeagueName", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("HomeTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("AwayTeam", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchDate", width=150, minwidth=150, anchor = tkinter.CENTER)
          tree.column("MatchVenue", width=400, minwidth=400, anchor = tkinter.CENTER)

          tree.heading("MatchID", text="Match ID", anchor = tkinter.CENTER)
          tree.heading("LeagueName", text="League Name", anchor = tkinter.CENTER)
          tree.heading("HomeTeam", text="Home Team", anchor = tkinter.CENTER)
          tree.heading("AwayTeam", text="Away Team", anchor = tkinter.CENTER)
          tree.heading("MatchDate", text="Date", anchor = tkinter.CENTER)
          tree.heading("MatchVenue", text="Venue/Stadium", anchor = tkinter.CENTER)

          i = 0
          for row in cs:
              tree.insert('', i, text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]) )
          vs = ttk.Scrollbar(r,orient="vertical")
          vs.configure(command=tree.yview)
          tree.configure(yscrollcommand=vs.set)
          vs.pack(fill="y",side="right")
          hsb = ttk.Scrollbar(r,orient='horizontal')
          hsb.configure(command=tree.xview)
          tree.configure(xscrollcommand=hsb.set)
          hsb.pack(fill="x",side="bottom")
          tree.pack()
          place_booking()
          break
          r.mainloop()
         
         else:
          print("Please enter a valid command and try again")
          continue

#module for checking user's booking history-------------------------------------------------------------------------------------------
def booking_history():
    global status
    global loggedin
    global accid
    while True:
       if status == 1:
          print("You are not currently logged in to any account, please log in to your account to view your booking history")
          break
       else:
          openingquery = 'SELECT AccID FROM accounts WHERE AccName = %s'
          cs.execute(openingquery, (loggedin,))
          opendata = cs.fetchall()
          accid = int(opendata[0][0])
          print("Displaying your booking history") 
          query = 'SELECT * FROM bookings WHERE AccID =%s'
          cs.execute(query, (accid,))
          bookingdata = cs.fetchall()
          for row in bookingdata:
             s = row[4]
             d = eval(s)
             date = row[2]
             ticksumm = '''Adult Priority - x'''+str(d.get("Adult(Priority)"))+''' 
                    Child Priority - x'''+str(d.get("Child(Priority)"))+'''
                    Adult Economy - x'''+str(d.get("Adult(Economy)"))+'''
                    Child Economy - x'''+str(d.get("Child(Economy)"))
             matchcardquery = 'SELECT HomeTeam, AwayTeam FROM fbmatches WHERE MatchID =%s'
             q = row[1]
             cs.execute(matchcardquery,(q,))
             matchcardrec = cs.fetchall()
             matchcardhome = []
             matchcardaway = []
             for rowe in matchcardrec:
                matchcardhome.append(rowe[0])
                matchcardaway.append(rowe[1])
             print('''                   Booking ID - ''',row[6],'''
                   Account ID -''',row[0],'''
                   Name - ''',row[5].upper(),'''
                   Match Code/ID - ''',row[1],'''
                   Match - ''',matchcardhome[0],'''(HOME) vs ''',matchcardaway[0],'''(AWAY)
                   Date and Time of booking - ''',date,'''
                   Ticket Summary: ''','''
                   ''',ticksumm,'''
                   Total Amt''',row[3])
          break


#module for cancelling bookings made by a user---------------------------------------------------------------------------------------
def booking_cancel():
   global status
   global loggedin
   global accid
   booking_history() 
   h = True
   while h == True:
    if status ==1:
      break
    else:
      intchoice = input('Do you want to delete a booking (y/n): ')
      if intchoice.lower() == "n":
         break
      elif intchoice.lower() == "y":
         intchoicedel = int(input("Please enter the Booking ID of the Booking you want to cancel: "))
         query = 'SELECT BookingID FROM bookings WHERE AccID = %s'
         cs.execute(query,(accid,))
         bookingidcollect = cs.fetchall() 
         bookingid = []
         for row in bookingidcollect:
            bookingid.append(row[0])  
         if intchoicedel not in bookingid:
            print("Incorrect booking ID entered, check the booking ID and try again")
            break
         else:
          while True:
            intchoicefinal = input('''This will permanently delete your booking
                                   Are you sure you want to proceed? (y/n)''')
            if intchoicefinal == "n":
               h = False
               break
            elif intchoicefinal =="y":
              delquery = 'DELETE FROM bookings WHERE BookingID = %s'
              cs.execute(delquery,(intchoicedel,))
              mycon.commit()
              print("Successfully deleted booking")
              print("Redirecting back to booking cancellation menu")
              h = True
              break
            else:
               print("Invalid option, select the correct command and try again")
               continue

#module for deleting user's account and all associated data--------------------------------------------------------------------------
def account_delete():
   global status
   global loggedin
   while True:
     if status == 1:
      print("You are not currently logged in to any account, Please log in first to delete your respective account")
      break
     else:
      intchoiceacc = input(''' IMPORTANT MESSAGE
            This will permanently delete your account and all its associated data (account metadata, booking history) from the Application database
            You will not be able to recover your account after this
            Are you sure you want to proceed?(y/n) ''')
      if intchoiceacc.lower() == "n":
         break
      elif intchoiceacc.lower() =="y":
         delquery1 = 'DELETE FROM bookings WHERE AccName =%s'
         cs.execute(delquery1,(loggedin,))
         delquery2 = 'DELETE FROM accounts WHERE AccName =%s'
         cs.execute(delquery2,(loggedin,))
         mycon.commit()
         print("Successfully deleted your account")
         status = 1
         loggedin = ""
         break
      

      

#main menu of the application--------------------------------------------------------------------------------------------------------
def main_menu():
    
    while True:
        print('''Welcome to the Ticket Booking Portal
              Please select which feature of the application you wish to use''')
        print("1. Create an account")
        print("2. Login/Logout")
        print("3. View matches and book tickets")
        print("4. View booking history")
        print("5. Cancel a ticket booking")
        print("6. Delete your account")
        print("7. Exit the application")
        choice = input("Enter your choice: ")

        if choice == "1":
            accountcrt()

        elif choice == "2":
            login_logout_module()

        elif choice == "3":
            booking_menu()
        
        elif choice == "4":
           booking_history()


        elif choice == "5":
           booking_cancel()

        elif choice == "6":
           account_delete()

        elif choice == "7":
            print("Exiting Application")
            break
        else:
            print("Invalid choice. Please try again.")

 
#running the application-------------------------------------------------------------------------------------------------------------
main_menu()  