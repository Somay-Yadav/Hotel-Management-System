import mysql.connector as myc
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# ================= HOTEL TITLE =================

print("""
╔══════════════════════════════════════╗
║        HOTEL MANAGEMENT SYSTEM       ║
╚══════════════════════════════════════╝
""")


# ================= CONNECT MYSQL =================

mydb = myc.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD")
)

cur = mydb.cursor()


# ================= DATABASE =================

cur.execute("CREATE DATABASE IF NOT EXISTS hotel_management")
cur.execute("USE hotel_management")


# ================= TABLES =================

cur.execute("""
CREATE TABLE IF NOT EXISTS login(
    username VARCHAR(30),
    password VARCHAR(30)
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS sno(
    customer_id INT,
    booking_id INT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS rooms(
    room_no INT PRIMARY KEY,
    room_type VARCHAR(30),
    price INT,
    status VARCHAR(30)
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INT PRIMARY KEY,
    name VARCHAR(30),
    age INT,
    gender CHAR(1),
    phone VARCHAR(10)
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    booking_id INT PRIMARY KEY,
    customer_id INT,
    room_no INT,
    check_in DATE,
    check_out DATE,
    total_bill INT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS room_prices(
    standard INT,
    deluxe INT,
    suite INT
)
""")


mydb.commit()



# ================= DEFAULT DATA =================


cur.execute("SELECT * FROM login")

if len(cur.fetchall()) == 0:

    cur.execute(
        "INSERT INTO login VALUES(%s,%s)",
        ("admin","1234")
    )



cur.execute("SELECT * FROM room_prices")

if len(cur.fetchall()) == 0:

    cur.execute(
        "INSERT INTO room_prices VALUES(2000,5000,10000)"
    )



cur.execute("SELECT * FROM rooms")

if len(cur.fetchall()) == 0:

    cur.execute(
        "INSERT INTO rooms VALUES(101,'Standard',2000,'Available')"
    )

    cur.execute(
        "INSERT INTO rooms VALUES(201,'Deluxe',5000,'Available')"
    )

    cur.execute(
        "INSERT INTO rooms VALUES(301,'Suite',10000,'Available')"
    )



cur.execute("SELECT * FROM sno")

if len(cur.fetchall()) == 0:

    cur.execute(
        "INSERT INTO sno VALUES(0,0)"
    )


mydb.commit()



print("""
╔════════════════════════╗
║     SYSTEM READY       ║
║   (DATABASE CREATED)   ║
║    (TABLES CREATED)    ║
║  (DEFAULT DATA ADDED)  ║
╚════════════════════════╝
""")



# ================= MAIN LOOP =================


while True:


    print("""
╔════════════════════════╗
║        MAIN MENU       ║
╠════════════════════════╣
║ 1. Login               ║
║ 2. Exit                ║
╚════════════════════════╝
""")


    ch=input("Enter choice: ")



    if ch=="1":


        pas=input("Enter Password: ")


        cur.execute("SELECT * FROM login")

        data=cur.fetchall()


        username,real_pass=data[0]


        if pas==real_pass:


            print("""
╔════════════════════════╗
║    LOGIN SUCCESSFUL    ║
╚════════════════════════╝
""")


            while True:


                print("""
╔══════════════════════════════════════╗
║             ADMIN PANEL              ║
╠══════════════════════════════════════╣
║ 1. Check-In Customer                 ║
║ 2. Add New Room                      ║
║ 3. Check-Out & Generate Bill         ║
║ 4. View Details                      ║
║ 5. Modify Details                    ║
║ 6. Change Password                   ║
║ 7. Logout                            ║
╚══════════════════════════════════════╝
""")


                adm=input("Enter choice: ")

                # ================= CHECK-IN =================

                if adm=="1":

                    print("""
                ╔════════════════════════════════╗
                ║        CUSTOMER CHECK-IN       ║
                ╚════════════════════════════════╝
                """)


                    cur.execute(
                        "SELECT * FROM rooms WHERE status='Available'"
                    )

                    available = cur.fetchall()


                    if len(available)==0:

                        print("No rooms available!")

                        continue



                    print("\nAVAILABLE ROOMS\n")

                    print(f"{'ROOM':<10}{'TYPE':<15}{'PRICE':<12}")
                    print("-"*40)


                    for r in available:

                        print(f"{r[0]:<10}{r[1]:<15}{r[2]:<12}")



                    room_no=int(input("\nEnter Room Number: "))



                    cur.execute(
                        "SELECT * FROM rooms WHERE room_no=%s AND status='Available'",
                        (room_no,)
                    )


                    room=cur.fetchall()



                    if len(room)==0:

                        print("Invalid room!")

                        continue



                    name=input("Name: ")
                    age=int(input("Age: "))
                    gender=input("Gender (M/F): ").upper()
                    phone=input("Phone: ")



                    cur.execute("SELECT * FROM sno")

                    sno=cur.fetchall()[0]


                    cust=sno[0]+1
                    book=sno[1]+1



                    today=datetime.date.today()



                    cur.execute(
                        "INSERT INTO customers VALUES(%s,%s,%s,%s,%s)",
                        (cust,name,age,gender,phone)
                    )


                    cur.execute(
                        """
                        INSERT INTO bookings
                        VALUES(%s,%s,%s,%s,NULL,NULL)
                        """,
                        (book,cust,room_no,today)
                    )



                    cur.execute(
                        "UPDATE rooms SET status='Booked' WHERE room_no=%s",
                        (room_no,)
                    )


                    cur.execute(
                        "UPDATE sno SET customer_id=%s,booking_id=%s",
                        (cust,book)
                    )


                    mydb.commit()



                    print(f"""
                ╔════════════════════════════════╗
                ║       CHECK-IN SUCCESSFUL      ║
                ╠════════════════════════════════╣
                ║ Customer ID : {cust:<10}       ║
                ║ Booking ID  : {book:<10}       ║
                ╚════════════════════════════════╝
                """)





                # ================= ADD ROOM =================


                elif adm=="2":


                    print("""
                ╔════════════════════════════════╗
                ║          ADD NEW ROOM          ║
                ╚════════════════════════════════╝
                """)


                    room_no=int(input("Room Number: "))

                    room_type=input(
                        "Room Type (Standard/Deluxe/Suite): "
                    ).capitalize()



                    cur.execute(
                        "SELECT * FROM room_prices"
                    )


                    prices=cur.fetchall()[0]


                    price={
                        "Standard":prices[0],
                        "Deluxe":prices[1],
                        "Suite":prices[2]
                    }



                    if room_type not in price:

                        print("Invalid type")

                        continue



                    cur.execute(
                        "INSERT INTO rooms VALUES(%s,%s,%s,%s)",
                        (
                            room_no,
                            room_type,
                            price[room_type],
                            "Available"
                        )
                    )



                    mydb.commit()



                    print("""
                ╔════════════════════════╗
                ║     ROOM ADDED         ║
                ╚════════════════════════╝
                """)






                # ================= CHECKOUT =================


                elif adm=="3":


                    print("""
                ╔════════════════════════════════╗
                ║          CHECK OUT             ║
                ╚════════════════════════════════╝
                """)


                    booking_id=int(input("Booking ID: "))



                    cur.execute(
                        """
                        SELECT * FROM bookings
                        WHERE booking_id=%s AND check_out IS NULL
                        """,
                        (booking_id,)
                    )



                    booking=cur.fetchall()



                    if len(booking)==0:

                        print("Invalid booking")

                        continue



                    booking=booking[0]



                    room_no=booking[2]

                    check_in=booking[3]

                    check_out=datetime.date.today()



                    days=(check_out-check_in).days



                    if days==0:

                        days=1



                    cur.execute(
                        "SELECT price FROM rooms WHERE room_no=%s",
                        (room_no,)
                    )



                    price=cur.fetchall()[0][0]



                    total=days*price




                    print(f"""
                ╔════════════════════════════╗
                ║          HOTEL BILL        ║
                ╠════════════════════════════╣
                ║ Room No     : {room_no:<10}   ║
                ║ Days Stayed : {days:<10}   ║
                ║ Price/Day   : {price:<10}   ║
                ║ Total Bill  : {total:<10}   ║
                ╚════════════════════════════╝
                """)



                    cur.execute(
                        """
                        UPDATE bookings
                        SET check_out=%s,total_bill=%s
                        WHERE booking_id=%s
                        """,
                        (check_out,total,booking_id)
                    )



                    cur.execute(
                        "UPDATE rooms SET status='Available' WHERE room_no=%s",
                        (room_no,)
                    )



                    mydb.commit()



                    print("CHECKOUT COMPLETE")
                
                # ================= VIEW DETAILS =================

                elif adm=="4":

                    print("""
                ╔════════════════════════════════╗
                ║          VIEW DETAILS          ║
                ╠════════════════════════════════╣
                ║ 1. Customers                   ║
                ║ 2. Rooms                       ║
                ║ 3. Current Bookings            ║
                ║ 4. Booking History             ║
                ╚════════════════════════════════╝
                """)


                    vv=input("Enter choice: ")



                    # -------- CUSTOMERS --------

                    if vv=="1":


                        cur.execute("SELECT * FROM customers")

                        customer_v=cur.fetchall()


                        print("""
                ╔════════════════════════════════════════════╗
                ║             CUSTOMER DETAILS               ║
                ╚════════════════════════════════════════════╝
                """)


                        print(
                            f"{'ID':<8}{'NAME':<20}{'AGE':<8}{'GENDER':<10}{'PHONE':<15}"
                        )

                        print("-"*65)



                        for r in customer_v:

                            print(
                                f"{r[0]:<8}{r[1]:<20}{r[2]:<8}{r[3]:<10}{r[4]:<15}"
                            )


                        print("-"*65)




                    # -------- ROOMS --------


                    elif vv=="2":


                        cur.execute("SELECT * FROM rooms")

                        room_v=cur.fetchall()



                        print("""
                ╔════════════════════════════════════════╗
                ║              ROOM DETAILS              ║
                ╚════════════════════════════════════════╝
                """)


                        print(
                            f"{'ROOM':<10}{'TYPE':<15}{'PRICE':<12}{'STATUS':<15}"
                        )

                        print("-"*55)



                        for r in room_v:

                            print(
                                f"{r[0]:<10}{r[1]:<15}{r[2]:<12}{r[3]:<15}"
                            )


                        print("-"*55)





                    # -------- CURRENT BOOKINGS --------


                    elif vv=="3":


                        cur.execute(
                            "SELECT * FROM bookings WHERE check_out IS NULL"
                        )

                        bookingv=cur.fetchall()



                        print("""
                ╔════════════════════════════════════════╗
                ║          CURRENT BOOKINGS              ║
                ╚════════════════════════════════════════╝
                """)


                        print(
                        f"{'BID':<8}{'CID':<8}{'ROOM':<8}{'CHECK-IN':<15}"
                        )

                        print("-"*45)



                        for r in bookingv:

                            print(
                            f"{r[0]:<8}{r[1]:<8}{r[2]:<8}{str(r[3]):<15}"
                            )


                        print("-"*45)




                    # -------- HISTORY --------


                    elif vv=="4":


                        cur.execute("SELECT * FROM bookings")

                        history=cur.fetchall()



                        print("""
                ╔════════════════════════════════════════╗
                ║          BOOKING HISTORY               ║
                ╚════════════════════════════════════════╝
                """)


                        print(
                        f"{'BID':<8}{'CID':<8}{'ROOM':<8}{'BILL':<10}"
                        )


                        print("-"*40)



                        for r in history:

                            print(
                            f"{r[0]:<8}{r[1]:<8}{r[2]:<8}{str(r[5]):<10}"
                            )


                        print("-"*40)





                # ================= MODIFY =================


                elif adm=="5":


                    print("""
                ╔════════════════════════════════╗
                ║          MODIFY MENU           ║
                ╠════════════════════════════════╣
                ║ 1. Change Room Prices          ║
                ║ 2. Modify Specific Room        ║
                ╚════════════════════════════════╝
                """)


                    mm=input("Enter choice: ")



                    if mm=="1":


                        std=int(input("Standard Price: "))
                        dlx=int(input("Deluxe Price: "))
                        ste=int(input("Suite Price: "))



                        cur.execute(
                        """
                        UPDATE room_prices
                        SET standard=%s,deluxe=%s,suite=%s
                        """,
                        (std,dlx,ste)
                        )



                        cur.execute(
                        "UPDATE rooms SET price=%s WHERE room_type='Standard'",
                        (std,)
                        )


                        cur.execute(
                        "UPDATE rooms SET price=%s WHERE room_type='Deluxe'",
                        (dlx,)
                        )


                        cur.execute(
                        "UPDATE rooms SET price=%s WHERE room_type='Suite'",
                        (ste,)
                        )



                        mydb.commit()



                        print("Prices Updated")




                    elif mm=="2":


                        room_no=int(input("Room Number: "))


                        cur.execute(
                        "SELECT * FROM rooms WHERE room_no=%s",
                        (room_no,)
                        )


                        room=cur.fetchall()



                        if len(room)==0:

                            print("Room not found")

                            continue



                        print("""
                1. Change Price
                2. Change Status
                """)


                        option=input("Choice: ")



                        if option=="1":


                            price=int(input("New Price: "))


                            cur.execute(
                            "UPDATE rooms SET price=%s WHERE room_no=%s",
                            (price,room_no)
                            )



                        elif option=="2":


                            status=input(
                            "Status (Available/Booked): "
                            )


                            cur.execute(
                            "UPDATE rooms SET status=%s WHERE room_no=%s",
                            (status,room_no)
                            )



                        mydb.commit()

                        print("Room Updated")





                # ================= PASSWORD =================


                elif adm=="6":


                    old=input("Current Password: ")



                    cur.execute("SELECT password FROM login")

                    real=cur.fetchall()[0][0]



                    if old==real:


                        new=input("New Password: ")


                        cur.execute(
                        "UPDATE login SET password=%s",
                        (new,)
                        )


                        mydb.commit()



                        print("""
                ╔════════════════════════╗
                ║ PASSWORD CHANGED       ║
                ╚════════════════════════╝
                """)


                    else:

                        print("Wrong Password")





                # ================= LOGOUT =================


                elif adm=="7":


                    print("""
                ╔════════════════════════╗
                ║       LOGGING OUT      ║
                ╚════════════════════════╝
                """)
                    break

    elif ch=="2":

        print("""
    ╔═════════════════════════════════╗
    ║                                 ║
    ║      EXITING SYSTEM...          ║
    ║                                 ║
    ║ THANK YOU FOR USING OUR SYSTEM! ║
    ║                                 ║
    ╚═════════════════════════════════╝
    """)

        break


    else:

        print("""
    ╔════════════════════════╗
    ║     INVALID CHOICE     ║
    ╚════════════════════════╝
    """)