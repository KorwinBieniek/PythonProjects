import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar
from fpdf import FPDF

WINDOW_SIZE = "600x400"


def register():
    global screen1
    screen1 = tk.Toplevel(screen)
    screen1.title("Rejestracja")
    screen1.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(screen1, text="Proszę o wprowadzenie danych poniżej").pack()
    tk.Label(screen1, text="").pack()
    tk.Label(screen1, text="Nazwa użytkownika * ").pack()
    username_entry = tk.Entry(screen1, textvariable=username)
    username_entry.pack()
    tk.Label(screen1, text="Hasło * ").pack()
    password_entry = tk.Entry(screen1, show="*", textvariable=password)
    password_entry.pack()
    tk.Label(screen1, text="").pack()
    tk.Button(screen1, text="Rejestracja", width=10, height=1, command=register_user).pack()


def register_user():
    username_info = username.get()
    password_info = password.get()

    with open(f'{username_info}.txt', "w") as file:
        file.write(username_info)
        file.write("\n")
        file.write(password_info)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    tk.Label(text="Rejestracja zakończona sukcesem")
    screen1.destroy()


def main_app():
    global window
    window = tk.Tk()
    window.title("Wypożyczalnia Samochodów")
    tk.Label(window,
             text="Wypożycz swój wymarzony samochód").pack()
    img = tk.PhotoImage(file='test_car.png')
    tk.Label(window, image=img).pack()
    window.geometry("660x360")
    window.configure(background="white")

    def connect_to_database():
        global cursor
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='car_rental',
                                                 user='root',
                                                 password='root',
                                                 autocommit=True)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()

        except mysql.connector.errors.ProgrammingError:
            connection = mysql.connector.connect(host='localhost',
                                                 database='sys',
                                                 user='root',
                                                 password='root',
                                                 autocommit=True)
            if connection.is_connected():

                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()

                def executeScriptsFromFile(filename):
                    fd = open(filename, 'r')
                    sqlFile = fd.read()
                    fd.close()
                    sqlCommands = sqlFile.split(';')

                    for command in sqlCommands:
                        try:
                            if command.strip() != '':
                                cursor.execute(command)
                        except IOError as msg:
                            print("Command skipped: ", msg)

                executeScriptsFromFile('C:/Users/admin/Desktop/TABProjekt/InitDatabase.sql')
                connection.commit()

        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        return connection, cursor

    def close_database_connection(connection):
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    def select_sample_vehicles_query():
        cursor.execute('''SELECT review.car_review_id, 
                            review.car_segment, 
                            vehicle.vehicle_type, vehicle.capacity, 
                            vehicle.manufactured_year, 
                            vehicle.sec_pay_status
                            FROM tbl_car_review review 
                            JOIN tbl_vehicle vehicle 
                            ON review.vehicle_id = vehicle .vehicle_id
                            WHERE 
                            vehicle.availability = TRUE;''')
        myresult = cursor.fetchall()
        outer_list = []
        columns = []
        counter = 0
        for x in myresult:
            for i in x:
                columns.append(str(i))
                counter += 1
                if counter == 6:
                    outer_list.append(columns)
                    columns = []
                    counter = 0
        return outer_list

    def add_customers_query(sample_name, sample_surname, sample_number, sample_address):
        cursor.execute(
            "INSERT INTO tbl_customer (name, surname, tel_number, addres) VALUES (%s, %s, %s, %s);",
            (sample_name, sample_surname, sample_number, sample_address))

    def add_rental_query(show_customers_screen, vehicle, customer, startDate, rdate_selection):
        cursor.execute(
            "INSERT INTO tbl_rental (vehicle_id, customer_id, rental_start_date, rental_return_date) VALUES (%s, %s, %s, %s);",
            (vehicle, customer, startDate, rdate_selection))
        cursor.execute(
            f"UPDATE tbl_vehicle SET availability = FALSE WHERE vehicle_id = {vehicle};")
        show_customers_screen.destroy()
        window.deiconify()

    def select_specific_customer(name, surname):
        cursor.execute(f'''SELECT * FROM tbl_customer WHERE name = '{name}' AND surname = '{surname}';''')
        myresult = cursor.fetchall()
        outer_list = []
        columns = []
        counter = 0
        for x in myresult:
            for i in x:
                columns.append(str(i))
                counter += 1
                if counter == 5:
                    outer_list.append(columns)
                    columns = []
                    counter = 0
        return outer_list

    def hide_main_window(second_window, main_window):
        main_window.deiconify()
        second_window.destroy()

    def add_return_button(return_window, main_window):
        return_button = tk.Button(
            return_window,
            text="Powrót",
            width=9,
            height=2,
            bg="white",
            fg="black",
            command=lambda: hide_main_window(return_window, main_window)
        )
        return_button.place(x=520, y=355)

    def show_cars(show_cars_window, date_selection, rdate_selection, select_car_bool):
        show_cars_screen = tk.Toplevel(show_cars_window)
        show_cars_screen.title("Tabela samochodów")
        show_cars_screen.geometry("800x280")
        result = select_sample_vehicles_query()
        my_tree = ttk.Treeview(show_cars_screen)
        my_tree.pack()

        my_tree['columns'] = ('ID', 'Car Segment', 'Vehicle Type',
                              'Capacity', 'Manufactured Year', 'Sec Pay Status')
        my_tree.column('#0', width=0, stretch=tk.NO)
        my_tree.column('ID', anchor=tk.W, width=100)
        my_tree.column('Car Segment', anchor=tk.W, width=100)
        my_tree.column('Vehicle Type', anchor=tk.CENTER, width=140)
        my_tree.column('Capacity', anchor=tk.CENTER, width=140)
        my_tree.column('Manufactured Year', anchor=tk.CENTER, width=140)
        my_tree.column('Sec Pay Status', anchor=tk.CENTER, width=140)

        my_tree.heading('ID', text='ID', anchor=tk.W)
        my_tree.heading('Car Segment', text='Car Segment', anchor=tk.W)
        my_tree.heading('Vehicle Type', text='Vehicle Type', anchor=tk.W)
        my_tree.heading('Capacity', text='Capacity', anchor=tk.W)
        my_tree.heading('Manufactured Year', text='Manufactured Year', anchor=tk.W)
        my_tree.heading('Sec Pay Status', text='Sec Pay Status', anchor=tk.W)

        counter = 0
        for record in result:
            if counter == 10:
                break
            my_tree.insert(parent='', index='end', values=record)
            counter += 1

        back_button = tk.Button(
            show_cars_screen,
            text="Poprzednia strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_previous_cars(my_tree, counter, result)
        )
        back_button.pack(side=tk.LEFT)

        next_button = tk.Button(
            show_cars_screen,
            text="Następna strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_next_cars(my_tree, counter, result)
        )
        next_button.pack(side=tk.LEFT)
        if select_car_bool:
            def selectItem():
                curItem = my_tree.focus()
                return my_tree.item(curItem)['values']

            select_button = tk.Button(
                show_cars_screen,
                text="Wybierz samochód",
                width=16,
                height=2,
                bg="white",
                fg="black",
                command=lambda: open_add_customer_window(date_selection, rdate_selection, show_cars_window, selectItem())
            )
            select_button.pack(side=tk.LEFT)

    def show_next_cars(my_tree, counter, result):

        my_tree.delete(*my_tree.get_children())

        new_counter = 0
        for record in result:
            if counter <= new_counter < counter + 10:
                my_tree.insert(parent='', index='end', values=record)
            new_counter += 1

    def show_previous_cars(my_tree, counter, result):

        my_tree.delete(*my_tree.get_children())

        new_counter = counter
        for record in result:
            if counter >= new_counter > counter - 10:
                my_tree.insert(parent='', index='end', values=record)
            new_counter -= 1

    def add_customer(add_customers_window, name, surname, number, address):

        add_customers_query(name, surname, number, address)
        tk.Label(add_customers_window,
                 text='Dodano klienta!').pack()

    # def select_customer(add_customers_window, name, surname):
    #
    #     result = str(select_specific_customer(name, surname))
    #     print(result)
    #     tk.Label(add_customers_window,
    #              text=result).pack()

    def open_rent_car_window(date_selection, rdate_selection):
        rent_car_window = tk.Toplevel(window)
        rent_car_window.title("Wypożycz Samochód")
        rent_car_window.geometry(WINDOW_SIZE)
        tk.Label(rent_car_window,
                 text="Tutaj możesz wypożyczyć samochód").pack()

        show_surnames_button = tk.Button(
            rent_car_window,
            text="Pokaż pojazdy",
            width=12,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_cars(rent_car_window, date_selection, rdate_selection, True)
        )
        show_surnames_button.pack()

        add_return_button(rent_car_window, window)
        window.iconify()

    def open_add_customer_window(date_selection, rdate_selection, show_cars_window, values):
        add_customer_window = tk.Toplevel(window)
        add_customer_window.title("Dodaj Klienta")
        add_customer_window.geometry(WINDOW_SIZE)
        label_frame = tk.Frame(add_customer_window)

        label_selection_frame = tk.Frame(add_customer_window)
        input_selection_frame = tk.Frame(add_customer_window)
        name_selection_label = tk.Label(label_selection_frame, text="Imię      ", font=("Courier", 12))
        surname_selection_label = tk.Label(input_selection_frame, text="Nazwisko   ", font=("Courier", 12))
        surname_selection_input = tk.Entry(input_selection_frame)
        name_selection_input = tk.Entry(label_selection_frame)
        name_selection_label.pack(side=tk.LEFT)
        surname_selection_label.pack(side=tk.LEFT)
        surname_selection_input.pack(side=tk.LEFT)
        name_selection_input.pack(side=tk.LEFT)
        label_selection_frame.pack()
        input_selection_frame.pack()

        tk.Label(add_customer_window,
                 text="Tutaj możesz wybrać klienta").pack()
        print(name_selection_input.get())
        add_customer_button = tk.Button(
            add_customer_window,
            text="Wybierz klienta",
            width=12,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_specific_customer_by_name(date_selection, rdate_selection, values, add_customer_window,
                                                           name_selection_input.get(),
                                                           surname_selection_input.get())
        )
        add_customer_button.pack()

        # Napisy nad entry fields
        car_data_label = tk.Label(label_frame, text=values)
        car_data_label.pack()
        name_label = tk.Label(label_frame, text="Imię      ", font=("Courier", 12))
        surname_label = tk.Label(label_frame, text="Nazwisko   ", font=("Courier", 12))
        number_label = tk.Label(label_frame, text="Numer tel   ", font=("Courier", 12))
        address_label = tk.Label(label_frame, text="Adres", font=("Courier", 12))
        name_label.pack(side=tk.LEFT)
        surname_label.pack(side=tk.LEFT)
        number_label.pack(side=tk.LEFT)
        address_label.pack(side=tk.LEFT)
        label_frame.pack()
        input_frame = tk.Frame(add_customer_window)
        name_input = tk.Entry(input_frame)
        surname_input = tk.Entry(input_frame)
        number_input = tk.Entry(input_frame)
        address_input = tk.Entry(input_frame)
        name_input.pack(side=tk.LEFT)
        surname_input.pack(side=tk.LEFT)
        number_input.pack(side=tk.LEFT)
        address_input.pack(side=tk.LEFT)
        input_frame.pack()

        add_customer_button = tk.Button(
            add_customer_window,
            text="Dodaj klienta",
            width=12,
            height=2,
            bg="white",
            fg="black",
            command=lambda: add_customer(add_customer_window, name_input.get(), surname_input.get(), number_input.get(),
                                         address_input.get())
        )
        add_customer_button.pack()

        add_return_button(add_customer_window, window)
        window.iconify()
        show_cars_window.destroy()

    def show_specific_customer_by_name(date_selection, rdate_selection, vehicle_data, add_customer_window, name_selection_input,
                                       surname_selection_input):
        result = select_specific_customer(name_selection_input,
                                          surname_selection_input)

        show_customers_screen = tk.Toplevel(add_customer_window)
        show_customers_screen.title("Tabela klientów")
        show_customers_screen.geometry("800x280")
        my_tree = ttk.Treeview(show_customers_screen)
        my_tree.pack()

        my_tree['columns'] = ('ID', 'Name', 'Surname',
                              'Phone Number', 'Address')
        my_tree.column('#0', width=0, stretch=tk.NO)
        my_tree.column('ID', anchor=tk.W, width=100)
        my_tree.column('Name', anchor=tk.W, width=100)
        my_tree.column('Surname', anchor=tk.CENTER, width=140)
        my_tree.column('Phone Number', anchor=tk.CENTER, width=140)
        my_tree.column('Address', anchor=tk.CENTER, width=140)

        my_tree.heading('ID', text='ID', anchor=tk.W)
        my_tree.heading('Name', text='Name', anchor=tk.W)
        my_tree.heading('Surname', text='Surname', anchor=tk.W)
        my_tree.heading('Phone Number', text='Phone Number', anchor=tk.W)
        my_tree.heading('Address', text='Address', anchor=tk.W)

        counter = 0
        for record in result:
            if counter == 10:
                break
            my_tree.insert(parent='', index='end', values=record)
            counter += 1

        def selectItem():
            curItem = my_tree.focus()
            return my_tree.item(curItem)['values']

        select_button = tk.Button(
            show_customers_screen,
            text="Wybierz klienta",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: add_rental_query(add_customer_window, vehicle_data[0],
                                             selectItem()[0], str(date_selection), str(rdate_selection))
        )
        select_button.pack(side=tk.LEFT)

    def open_show_customers_window():
        show_customers_window = tk.Toplevel(window)
        show_customers_window.title("Zwróć pojazd")
        show_customers_window.geometry(WINDOW_SIZE)
        tk.Label(show_customers_window,
                 text="Tutaj możesz zwrócić pojazd").pack()
        show_surnames_button = tk.Button(
            show_customers_window,
            text="Zwróć pojazd",
            width=12,
            height=2,
            bg="white",
            fg="black",
            command=lambda: open_return_car_date(show_customers_window)
        )
        show_surnames_button.pack()
        add_return_button(show_customers_window, window)
        window.iconify()

    # def open_reserve_car_window():
    #     show_reserve_car_window = tk.Toplevel(window)
    #     show_reserve_car_window.title("Zarezerwuj samochód")
    #     show_reserve_car_window.geometry(WINDOW_SIZE)
    #     tk.Label(show_reserve_car_window,
    #              text="Tutaj możesz zarezerwować samochód").pack()
    #
    #     show_reserve_car_button = tk.Button(
    #         show_reserve_car_window,
    #         text="Zarezerwuj samochód",
    #         width=18,
    #         height=2,
    #         bg="white",
    #         fg="black",
    #     )
    #     show_reserve_car_button.pack()
    #     add_return_button(show_reserve_car_window, window)
    #     window.iconify()

    def open_select_date_window():
        date_selection = return_date_selection()
        rdate_selection = return_date_selection()
        open_rent_car_window(date_selection, rdate_selection)

    def open_return_car_date(show_customers_window):
        date_selection = return_date_selection()
        open_return_car_window(show_customers_window, date_selection)

    def open_return_car_window(show_customers_window, date_selection):
        show_cars_screen = tk.Toplevel(show_customers_window)
        show_cars_screen.title("Tabela wynajmu")
        show_cars_screen.geometry("1000x280")
        result = select_rented_query_not_returned()
        my_tree = ttk.Treeview(show_cars_screen)
        my_tree.pack()

        my_tree['columns'] = ('ID', 'Car Segment', 'Vehicle Type',
                              'Capacity', 'Manufactured Year', 'Sec Pay Status', 'Rental Date')
        my_tree.column('#0', width=0, stretch=tk.NO)
        my_tree.column('ID', anchor=tk.W, width=100)
        my_tree.column('Car Segment', anchor=tk.W, width=100)
        my_tree.column('Vehicle Type', anchor=tk.CENTER, width=140)
        my_tree.column('Capacity', anchor=tk.CENTER, width=140)
        my_tree.column('Manufactured Year', anchor=tk.CENTER, width=140)
        my_tree.column('Sec Pay Status', anchor=tk.CENTER, width=140)
        my_tree.column('Rental Date', anchor=tk.CENTER, width=140)

        my_tree.heading('ID', text='ID Klienta', anchor=tk.W)
        my_tree.heading('Car Segment', text='Imię', anchor=tk.W)
        my_tree.heading('Vehicle Type', text='Nazwisko', anchor=tk.W)
        my_tree.heading('Capacity', text='ID Pojazdu', anchor=tk.W)
        my_tree.heading('Manufactured Year', text='Typ pojazdu', anchor=tk.W)
        my_tree.heading('Sec Pay Status', text='Pojemność', anchor=tk.W)
        my_tree.heading('Rental Date', text='Data wynajmu', anchor=tk.W)

        counter = 0
        for record in result:
            if counter == 10:
                break
            my_tree.insert(parent='', index='end', values=record)
            counter += 1

        back_button = tk.Button(
            show_cars_screen,
            text="Poprzednia strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_previous_cars_rental(my_tree, counter, result)
        )
        back_button.pack(side=tk.LEFT)

        next_button = tk.Button(
            show_cars_screen,
            text="Następna strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_next_cars_rental(my_tree, counter, result)
        )
        next_button.pack(side=tk.LEFT)

        def selectItem():
            curItem = my_tree.focus()
            return my_tree.item(curItem)['values']

        select_button = tk.Button(
            show_cars_screen,
            text="Wybierz samochód",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: add_return_query(date_selection, show_cars_screen, selectItem())
        )
        select_button.pack(side=tk.LEFT)

        cancel_button = tk.Button(
            show_cars_screen,
            text="Anuluj rezerwację",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: cancel_reservation_query(show_cars_screen, selectItem())
        )
        cancel_button.pack(side=tk.LEFT)

    def cancel_reservation_query(show_customers_screen, vehicle):
        vehicle = vehicle[3]
        cursor.execute(
            f"UPDATE tbl_rental SET rental_return_date = '2000-01-01' WHERE vehicle_id = {vehicle};")
        cursor.execute(
            f"UPDATE tbl_vehicle SET availability = TRUE WHERE vehicle_id = {vehicle};")

        messagebox.showinfo(title='Informacja', message=f'Rezerwacja została anulowana')

        show_customers_screen.destroy()

    def add_return_query(date_selection, show_customers_screen, vehicle):
        vehicle = vehicle[3]
        cursor.execute(
            f"UPDATE tbl_rental SET rental_return_date = '{date_selection}' WHERE vehicle_id = {vehicle};")
        cursor.execute(
            f"UPDATE tbl_vehicle SET availability = TRUE WHERE vehicle_id = {vehicle};")

        cursor.execute(f'''SELECT DATEDIFF(rental_return_date, rental_start_date) * 60 * (1.2 * ASCII(tbl_vehicle.vehicle_type) / 100) FROM tbl_rental
                            JOIN tbl_vehicle
                            ON tbl_rental.vehicle_id = tbl_vehicle.vehicle_id
                            WHERE tbl_rental.vehicle_id = {vehicle};''')
        myresult = cursor.fetchall()
        messagebox.showinfo(title='Zapłata', message=f'Musisz zapłacić {round(myresult[0][0], 2)} zł.')

        show_customers_screen.destroy()

    def return_date_selection():
        def cal_done():
            top.withdraw()
            root.quit()

        root = tk.Tk()
        root.title('Wybierz datę')
        root.withdraw()

        top = tk.Toplevel(root)

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="Wybierz datę", command=cal_done).pack()

        selected_date = None
        root.mainloop()
        return cal.selection_get()

    # def show_reservation(show_check_reservations_window):
    #     result = str(select_rented_query())
    #     tk.Label(show_check_reservations_window,
    #              text=result).pack()

    def select_rented_query():
        cursor.execute(f'''SELECT customer.customer_id, customer.name, 
                            customer.surname, 
                            vehicle.vehicle_id, 
                            vehicle.vehicle_type, 
                            vehicle.capacity, 
                            rental.rental_start_date, 
                            rental_return_date
                            FROM tbl_vehicle vehicle 
                            JOIN tbl_rental rental 
                            ON vehicle.vehicle_id = rental.vehicle_id
                            JOIN tbl_customer customer 
                            ON customer.customer_id = rental.customer_id
                            ORDER BY rental_id DESC;''')
        myresult = cursor.fetchall()
        outer_list = []
        columns = []
        counter = 0
        for x in myresult:
            for i in x:
                columns.append(str(i))
                counter += 1
                if counter == 8:
                    outer_list.append(columns)
                    columns = []
                    counter = 0
        return outer_list

    def select_rented_query_not_returned():
        cursor.execute(f'''SELECT customer.customer_id, customer.name, 
                            customer.surname, 
                            vehicle.vehicle_id, 
                            vehicle.vehicle_type, 
                            vehicle.capacity, 
                            rental.rental_start_date, 
                            rental_return_date
                            FROM tbl_vehicle vehicle 
                            JOIN tbl_rental rental 
                            ON vehicle.vehicle_id = rental.vehicle_id
                            JOIN tbl_customer customer 
                            ON customer.customer_id = rental.customer_id
                            ORDER BY rental_id DESC;''')
        myresult = cursor.fetchall()
        outer_list = []
        columns = []
        counter = 0
        for x in myresult:
            for i in x:
                columns.append(str(i))
                counter += 1
                if counter == 8:
                    outer_list.append(columns)
                    columns = []
                    counter = 0
        return outer_list

    def show_rented_cars(show_cars_window):
        show_cars_screen = tk.Toplevel(show_cars_window)
        show_cars_screen.title("Tabela wynajmu")
        show_cars_screen.geometry("1080x280")
        result = select_rented_query()
        my_tree = ttk.Treeview(show_cars_screen)
        my_tree.pack()

        my_tree['columns'] = ('ID', 'Car Segment', 'Vehicle Type',
                              'Capacity', 'Manufactured Year', 'Sec Pay Status', 'Rental Date', 'Rental Return')
        my_tree.column('#0', width=0, stretch=tk.NO)
        my_tree.column('ID', anchor=tk.W, width=100)
        my_tree.column('Car Segment', anchor=tk.W, width=100)
        my_tree.column('Vehicle Type', anchor=tk.CENTER, width=140)
        my_tree.column('Capacity', anchor=tk.CENTER, width=140)
        my_tree.column('Manufactured Year', anchor=tk.CENTER, width=140)
        my_tree.column('Sec Pay Status', anchor=tk.CENTER, width=140)
        my_tree.column('Rental Date', anchor=tk.CENTER, width=140)
        my_tree.column('Rental Return', anchor=tk.CENTER, width=140)

        my_tree.heading('ID', text='ID Klienta', anchor=tk.W)
        my_tree.heading('Car Segment', text='Imię', anchor=tk.W)
        my_tree.heading('Vehicle Type', text='Nazwisko', anchor=tk.W)
        my_tree.heading('Capacity', text='ID Pojazdu', anchor=tk.W)
        my_tree.heading('Manufactured Year', text='Typ pojazdu', anchor=tk.W)
        my_tree.heading('Sec Pay Status', text='Pojemność', anchor=tk.W)
        my_tree.heading('Rental Date', text='Data wynajmu', anchor=tk.W)
        my_tree.heading('Rental Return', text='Data zwrotu', anchor=tk.W)

        counter = 0
        for record in result:
            if counter == 10:
                break
            my_tree.insert(parent='', index='end', values=record)
            counter += 1

        back_button = tk.Button(
            show_cars_screen,
            text="Poprzednia strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_previous_cars_rental(my_tree, counter, result)
        )
        back_button.pack(side=tk.LEFT)

        next_button = tk.Button(
            show_cars_screen,
            text="Następna strona",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_next_cars_rental(my_tree, counter, result)
        )
        next_button.pack(side=tk.LEFT)

    def show_next_cars_rental(my_tree, counter, result):
        my_tree.delete(*my_tree.get_children())
        new_counter = 0
        for record in result:
            if counter <= new_counter < counter + 10:
                my_tree.insert(parent='', index='end', values=record)
            new_counter += 1

    def show_previous_cars_rental(my_tree, counter, result):
        my_tree.delete(*my_tree.get_children())
        new_counter = counter
        for record in result:
            if counter >= new_counter > counter - 10:
                my_tree.insert(parent='', index='end', values=record)
            new_counter -= 1

    def open_check_reservations_window():
        show_check_reservations_window = tk.Toplevel(window)
        show_check_reservations_window.title("Wyświetl rezerwacje")
        show_check_reservations_window.geometry(WINDOW_SIZE)
        tk.Label(show_check_reservations_window,
                 text="Tutaj możesz wyświetlić/usunąć rezerwacje").pack()
        show_check_reservations_button = tk.Button(
            show_check_reservations_window,
            text="Pokaż rezerwacje",
            width=16,
            height=2,
            bg="white",
            fg="black",
            command=lambda: show_rented_cars(show_check_reservations_window)
        )
        show_check_reservations_button.pack()
        add_return_button(show_check_reservations_window, window)
        window.iconify()

    def print_rental():
        content = select_rented_query()
        with open("reservation.txt", "w") as file:
            for reservation in content:
                for element in reservation:
                    file.write(element + ";")
                file.write("\n")
        from fpdf import FPDF
        pdf = FPDF()

        pdf.add_page()
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt='Reservation Raport\n', ln=1, align='C')

        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt='Rental ID | Customer ID | Vehicle ID | Booking ID | Rental Start Date | Rental Return Date\n', ln=1, align='L')


        file = open("reservation.txt", "r")

        for g in file:
            pdf.cell(200, 10, txt=g + "\n", ln=1, align='L')

        pdf.output("Reservation_raport.pdf")


    def create_main():
        button_frame = tk.Frame()

        generate_raport_button = tk.Button(
            master=button_frame,
            text="Generuj raport",
            width=17,
            height=5,
            bg="white",
            fg="black",
            command=lambda: print_rental()
        )

        add_customer_button = tk.Button(
            master=button_frame,
            text="Katalog pojazdów",
            width=17,
            height=5,
            bg="white",
            fg="black",
            command=lambda: show_cars(window, '01-01-2010', False)
        )

        rent_car_button = tk.Button(
            master=button_frame,
            text="Wypożycz samochód",
            width=17,
            height=5,
            bg="white",
            fg="black",
            command=open_select_date_window
        )

        return_car_button = tk.Button(
            master=button_frame,
            text="Zwróć samochód",
            width=17,
            height=5,
            bg="white",
            fg="black",
            command=open_show_customers_window
        )

        # reserve_car_button = tk.Button(
        #     master=button_frame,
        #     text="Zarezerwuj samochód",
        #     width=22,
        #     height=5,
        #     bg="white",
        #     fg="black",
        #     command=open_reserve_car_window
        # )

        check_reservations_button = tk.Button(
            master=button_frame,
            text="Sprawdź rezerwacje",
            width=17,
            height=5,
            bg="white",
            fg="black",
            command=open_check_reservations_window
        )

        add_customer_button.pack(side=tk.LEFT)
        rent_car_button.pack(side=tk.LEFT)
        return_car_button.pack(side=tk.LEFT)
        # reserve_car_button.pack(side=tk.LEFT)
        check_reservations_button.pack(side=tk.LEFT)
        generate_raport_button.pack(side=tk.LEFT)
        #show_help_button.pack(side=tk.RIGHT)

        button_frame.pack(fill=tk.X)
        #help_frame.pack(fill=tk.Y)

    conn, cursor = connect_to_database()
    create_main()
    window.mainloop()
    close_database_connection(conn)


def log_user(password_processing, username_processing):
    username_info = username.get()
    password_info = password.get()
    try:
        with open(f'{username_info}.txt', "r") as file:

            credentials = file.readlines()

            if password_info == credentials[1]:
                screen.destroy()
                main_app()
            else:
                username_processing.config(text="")
                password_processing.config(text='Błędne hasło')
    except FileNotFoundError:
        password_processing.config(text="")
        username_processing.config(text='Błędna nazwa użytkownika')


def login():
    global screen1
    screen1 = tk.Toplevel(screen)
    screen1.title("Logowanie")
    screen1.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(screen1, text="Proszę o wprowadzenie danych poniżej").pack()
    tk.Label(screen1, text="").pack()
    tk.Label(screen1, text="Nazwa użytkownika * ").pack()
    username_entry = tk.Entry(screen1, textvariable=username)
    username_entry.pack()
    tk.Label(screen1, text="Hasło * ").pack()
    password_entry = tk.Entry(screen1, show="*", textvariable=password)
    password_entry.pack()
    password_processing = tk.Label(screen1, text="")
    password_processing.pack()
    username_processing = tk.Label(screen1, text="")
    username_processing.pack()
    tk.Button(screen1, text="Logowanie", width=10, height=1,
              command=lambda: log_user(password_processing, username_processing)).pack()

def show_help(window):
    help_window = tk.Toplevel(window)
    help_window.title("Pomoc")
    help_window.geometry("800x400")

    firstLabel = tk.Label(help_window, text="""Instrukcja użytkownika

Aby skorzystać z aplikacji wpisz swój login i hasło, jeżeli jeszcze nie posiadasz konta - zarejestruj się.
Aby sprawdzić pojazdy dostępne w bazie kliknij "Katalog pojazdów"
Aby sprawdzić obecne/aktualne rezerwację kliknij "Sprawdź rezerwacje"
Aby wypożyczyć samochód klientowi wybierz "Wypożycz samochód", następnie wybierz datę od której będzie wypożyczony pojazd, 
po wybraniu daty pojawia się okienko z przyciskiem "Pokaż pojazdy", 
po kliknięciu w przycisk wybieramy interesujący klienta samochód zaznaczając go myszką, 
a następnie klikamy "Wybierz samochód", wyświetli się nam panel danych klienta, 
jeżeli klient istnieje w bazie to możemy wyszukać jego dane wpisując Imię i Nazwisko na następnie klikając "Wybierz klienta", 
jeżeli klient istnieje w bazie, to pokaże nam się w osobnym panelu, wybierając klienta przypisujemy go do wybranego wcześniej samochodu, 
jeżeli klienta nie ma w bazie to możemy wpisać jego dane poniżej, 
kliknięcie "Dodaj klienta" spowoduje dodanie go do bazy danych wraz z możliwością 
wyboru tego klienta i przypisania go do wybranego wcześniej samochodu, 
podobnie jak to miało miejsce w przypadku klienta, który był już w bazie.

Po kliknięciu "Sprawdź rezerwacje", pierwszy rekord tabeli pokazuje "najświeższą" rezerwację. 
W przypadku zgłoszenia zwrotu pojazdu klikamy "Zwróć pojazd", w wyświetlonym panelu klikamy ponownie "Zwróć pojazd", 
następnie zaznaczamy na kalendarzu datę zwrotu samochodu przez klienta i klikamy ok, 
wybieramy z listy "Tabeli wynajmu" samochód do zwrotu i klikamy "Wybierz samochód", 
zostaje naliczona opłata, po kliknięciu "ok" zwrot zostaje zatwierdzony.
""")
    firstLabel.pack()

def main_screen():
    global screen
    screen = tk.Tk()
    screen.geometry("300x250")
    screen.title("Wypożyczalnia Samochodów - autoryzacja")
    tk.Label(text="Autoryzacja", bg="grey", width="300", height="2", font=("Calibry", 13)).pack()
    tk.Label(screen, text="").pack()
    tk.Button(screen, text="Logowanie", width=30, height=2, command=login).pack()
    tk.Label(screen, text="").pack()
    tk.Button(screen, text="Rejestracja", width=30, height=2, command=register).pack()
    tk.Label(screen, text="Instrukcja Użytkownika").pack()
    show_help_button = tk.Button(
        master=screen,
        text="Pomoc",
        width=30,
        height=2,
        command=lambda: show_help(screen)
    )
    show_help_button.pack()
    screen.mainloop()


main_screen()
