import json
import os


def add_expense():
    name = input('Enter name: ')
    amount = input('Enter amount: ')

    while not amount.isdigit():
        amount = input('Enter amount: ')

    expenses = {'name': name, 'amount': amount}
    return expenses


if not os.path.exists('Budget_Calculator'):
    os.makedirs('Budget_Calculator')

budget_list = None

while True:
    expenses = []

    while budget_list is None:
        budget_lists = os.listdir('Budget_Calculator')
        count_budget_list = 0
        for budget in budget_lists:
            count_budget_list += 1
            print(f'{count_budget_list}. {budget}')

        print('\n1. Choose'
              '\n2. Add'
              '\n3. Delete'
              '\n4. Change'
              '\n5. Exit')
        choice = input('choose action: ')

        if choice == '1':
            choice_list = int(input('choice list: ')) - 1
            budget_list = budget_lists[choice_list]
        elif choice == '2':
            list_name = input('Enter list name: ')
            with open(f'Budget_Calculator/{list_name}.json', 'w', encoding='utf-8') as expenses_json:
                new_list = []
                json.dump(new_list, expenses_json, ensure_ascii=False, indent=4)
        elif choice == '3':
            choice = int(input('Enter number: ')) - 1
            choice_del = input(f'Are you sure you want to delete: {budget_lists[choice]}(y/n): ')
            if choice_del == 'y':
                os.remove(f'Budget_Calculator/{budget_lists[choice]}')
        elif choice == '4':
            choice = int(input('Enter number: ')) - 1
            new_name = input('Enter new name: ')
            os.rename(f'Budget_Calculator/{budget_lists[choice]}', new_name)
        elif choice == '5':
            break
        else:
            print('Invalid choice. Please select a number between 1 and 5.')

    while budget_list is not None:
        expenses_json_r = open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8')
        expenses = json.load(expenses_json_r)
        count = 0
        count_expenses = 0
        print('\n')
        for expense in expenses:
            count += 1
            if str(eval(expense["amount"])) != expense["amount"]:
                print(f'{count}: {expense["name"].capitalize()}: {expense["amount"]} = {eval(expense["amount"])}')
            else:
                print(f'{count}: {expense["name"].capitalize()}: {expense["amount"]}')
            count_expenses += int(eval(expense["amount"]))
        print('\nsum =', count_expenses)

        print('\n1. Add'
              '\n2. Delete'
              '\n3. Change name'
              '\n4. Change amount'
              '\n5. sum expenses'
              '\n6. sum incomes'
              '\n7. Exit')
        choice = input('choose action: ')

        if choice == '1':
            expenses.append(add_expense())
            with open(f'Budget_Calculator/{budget_list}', 'w', encoding='utf-8') as expenses_json:
                json.dump(expenses, expenses_json, ensure_ascii=False, indent=4)
        elif choice == '2':
            choice = int(input('Enter number: ')) - 1
            choice_del = input(f'Are you sure you want to delete: {expenses[choice]["name"].capitalize()} (y/n): ')
            if choice_del == 'y':
                expenses.pop(choice)
                with open(f'Budget_Calculator/{budget_list}', 'w', encoding='utf-8') as expenses_json:
                    json.dump(expenses, expenses_json, indent=4)

        elif choice == '3':
            choice = int(input('Enter number: ')) - 1
            new_name = input(f'Enter name({expenses[choice]["name"].capitalize()}): ')
            change = {'name': new_name,
                      'amount': f'{expenses[choice]["amount"]}'}
            expenses.pop(choice)
            expenses.insert(choice, change)
            with open(f'Budget_Calculator/{budget_list}', 'w', encoding='utf-8') as expenses_json:
                json.dump(expenses, expenses_json, indent=4)
        elif choice == '4':
            choice = int(input('Enter number: ')) - 1
            new_amount = input(f'Enter amount({expenses[choice]["amount"]}): ')
            change = {'name': expenses[choice]["name"].capitalize(),
                      'amount': new_amount}
            expenses.pop(choice)
            expenses.insert(choice, change)
            with open(f'Budget_Calculator/{budget_list}', 'w', encoding='utf-8') as expenses_json:
                json.dump(expenses, expenses_json, indent=4)

        elif choice == '5':
            with open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8') as expenses_json:
                expenses = json.load(expenses_json)
                count = 0
                for expense in expenses:
                    if int(expense["amount"]) > 0:
                        count += int(expense["amount"])
            print(f'\nexpenses = {count}\n')

        elif choice == '6':
            with open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8') as expenses_json:
                expenses = json.load(expenses_json)
                count = 0
                for expense in expenses:
                    if int(expense["amount"]) < 0:
                        count += int(expense["amount"])
            print(f'\nincomes = {count * -1}\n')
        elif choice == '7':
            break
        else:
            print('Invalid choice. Please select a number between 1 and 6.')
    break
