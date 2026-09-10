def select_menu_option():
    option_number = 0
    while True:
        if option_number > 0 and option_number < 5:
            break
        else:
            try:
                option_number = int(input("Select option: "))
            except:
                print("Input must be a valid number")
    print(option_number)


def display_menu():
    print("\nPersonal Library Manager")
    print("1. Add book")
    print("2. Remove book")
    print("3. List books")
    print("4. Exit")
    select_menu_option()
    
    
def main():
    display_menu()
    
    
if __name__ == "__main__":
    main()