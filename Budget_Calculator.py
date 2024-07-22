import json
import os


def add_expense(type, list=None):
    name = input('Enter name: ')
    amount = input('Enter amount: ')

    result = 0

    if list is not None:
        expenses = {'name': name, 'amount': amount, 'result': result, 'type': type, 'list': list}
    else:
        expenses = {'name': name, 'amount': amount, 'type': type}

    return expenses


def save_expense(expenses):
    with open(f'Budget_Calculator/{budget_list}', 'w', encoding='utf-8') as expenses_json:
        json.dump(expenses, expenses_json, ensure_ascii=False, indent=4)


if not os.path.exists('Budget_Calculator'):
    os.makedirs('Budget_Calculator')

budget_list = None

while True:
    expenses = []

    while budget_list is None:
        budget_lists = os.listdir('Budget_Calculator')
        count_budget_list = 0
        print('\n')
        for budget in budget_lists:
            count_budget_list += 1
            print(f'{count_budget_list}. {budget}')

        print('\n1. Choose'
              '\n2. Add'
              '\n3. Delete'
              '\n4. Change name'
              '\n5. Unite'
              '\n6. Exit')
        choice = input('choose action: ')

        # Choose
        if choice == '1':
            choice = int(input('choice list: ')) - 1
            budget_list = budget_lists[choice]
        # Add
        elif choice == '2':
            list_name = input('Enter list name: ')
            with open(f'Budget_Calculator/{list_name}.json', 'w', encoding='utf-8') as expenses_json:
                new_list = []
                json.dump(new_list, expenses_json, ensure_ascii=False, indent=4)
        # Delete
        elif choice == '3':
            choice = int(input('Enter number: ')) - 1
            choice_del = input(f'Are you sure you want to delete: {budget_lists[choice][:-5]}(y/n): ')
            if choice_del == 'y':
                os.remove(f'Budget_Calculator/{budget_lists[choice]}')
        # Change name
        elif choice == '4':
            choice = int(input('Enter number: ')) - 1
            new_name = input(f'Enter new name({budget_lists[choice][:-5]}): ')
            os.rename(f'Budget_Calculator/{budget_lists[choice]}', f'Budget_Calculator/{new_name}.json')
        # Unite
        elif choice == '5':
            choice_first = int(input('Enter first number: ')) - 1
            choice_second = int(input('Enter second number: ')) - 1
            print(f'\n1. append {budget_lists[choice_second]} to {budget_lists[choice_first]}'
                  f'\n2. append {budget_lists[choice_second]} to {budget_lists[choice_first]} and delete {budget_lists[choice_second]}'
                  f'\n3. append {budget_lists[choice_first]} to {budget_lists[choice_second]}'
                  f'\n4. append {budget_lists[choice_first]} to {budget_lists[choice_second]} and delete {budget_lists[choice_first]}'
                  f'\n5. unite {budget_lists[choice_first]} and {budget_lists[choice_second]} to new list'
                  f'\n6. unite {budget_lists[choice_first]} and {budget_lists[choice_second]} to new list and delete olds'
                  f'\n7. Exit')
            choice = input('Enter number: ')

            if choice == '7':
                continue

            with open(f'Budget_Calculator/{budget_lists[choice_first]}', 'r', encoding='utf-8') as expenses_first_json_r:
                expenses_first = json.load(expenses_first_json_r)
            expenses_first_json_w = open(f'Budget_Calculator/{budget_lists[choice_first]}', 'w', encoding='utf-8')
            expenses_second_json_r = open(f'Budget_Calculator/{budget_lists[choice_second]}', 'r', encoding='utf-8')
            expenses_second_json_w = open(f'Budget_Calculator/{budget_lists[choice_second]}', 'w', encoding='utf-8')
            expenses_second = json.load(expenses_second_json_r)

            # second to first
            if choice == '1':
                for expense in expenses_second:
                    expenses_first.append(expense)
                json.dump(expenses_first, expenses_first_json_w, ensure_ascii=False, indent=4)
            # second to first delete
            elif choice == '2':
                for expense in expenses_second:
                    expenses_first.append(expense)
                json.dump(expenses_first, expenses_first_json_w, ensure_ascii=False, indent=4)
                os.remove(f'Budget_Calculator/{budget_lists[choice_second]}')
            # first to second
            elif choice == '3':
                for expense in expenses_first:
                    expenses_second.append(expense)
                json.dump(expenses_second, expenses_second_json_w, ensure_ascii=False, indent=4)
            # first to second delete
            elif choice == '4':
                for expense in expenses_second:
                    expenses_first.append(expense)
                json.dump(expenses_second, expenses_first_json_w, ensure_ascii=False, indent=4)
                os.remove(f'Budget_Calculator/{budget_lists[choice_first]}')
            # unite
            elif choice == '5':
                new_list = []
                for expense in expenses_first and expenses_second:
                    new_list.append(expense)
            # unite delete
            elif choice == '6':
                new_list = []
                for expense in expenses_first and expenses_second:
                    new_list.append(expense)
                os.remove(f'Budget_Calculator/{budget_lists[choice_first]}')
                os.remove(f'Budget_Calculator/{budget_lists[choice_second]}')
            else:
                print('Invalid choice. Please select a number between 1 and 7.')

            expenses_first_json_r.close()
            expenses_first_json_w.close()
            expenses_second_json_r.close()
            expenses_second_json_w.close()

        # Exit
        elif choice == '6':
            break
        else:
            print('Invalid choice. Please select a number between 1 and 6.')

    while budget_list is not None:
        with open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8') as expenses_json_r:
            expenses = json.load(expenses_json_r)
        count = 0
        count_expenses = 0
        print('\n')
        for expense in expenses:
            count += 1

            if "list" in expense:
                with open(f'Budget_Calculator/{expense["list"]}', 'r', encoding='utf-8') as expenses_json_r_add:
                    expenses_add = json.load(expenses_json_r_add)
                    count_expenses_add = 0
                    for expense_add in expenses_add:
                        if expense_add["type"] == 'expense':
                            count_expenses_add -= int(eval(expense_add["amount"]))
                        elif expense_add["type"] == 'income':
                            count_expenses_add += int(eval(expense_add["amount"]))
                    if count_expenses_add != expense["result"]:
                        expense["result"] = count_expenses_add

            if "list" in expense:
                print(f'{count}: {expense["name"].capitalize()}: {expense["amount"]}{expense["result"]} = {round(eval(f'{expense["amount"]} {expense["result"]}'), 2)}')
            elif str(eval(expense["amount"])) != expense["amount"]:
                print(f'{count}: {expense["name"].capitalize()}: {expense["amount"]} = {round(eval(expense["amount"]), 2)}')
            else:
                print(f'{count}: {expense["name"].capitalize()}: {expense["amount"]}')

            if expense["type"] == 'expense':
                count_expenses -= int(eval(expense["amount"]))
            elif expense["type"] == 'income':
                count_expenses += int(eval(expense["amount"]))
        print('\nsum =', count_expenses)

        print('\n1. Add'
              '\n2. Add another list'
              '\n3. Delete'
              '\n4. Change name'
              '\n5. Change amount'
              '\n6. sum expenses'
              '\n7. sum incomes'
              '\n8. Back'
              '\n9. Exit')
        choice = input('choose action: ')

        # Add
        if choice == '1':
            print('\n1. expense'
                  '\n2. income')
            choice = input('choose: ')
            if choice == '1':
                expenses.append(add_expense('expense'))
            elif choice == '2':
                expenses.append(add_expense('income'))

            save_expense(expenses)
        # Add another list
        elif choice == '2':
            print('\n1. expense'
                  '\n2. income')
            choice = input('choose: ')

            count_budget_list = 0
            print('\n')
            for budget in budget_lists:
                count_budget_list += 1
                print(f'{count_budget_list}. {budget}')
            while True:
                choice_list = int(input('choose: ')) - 1
                if budget_lists[choice_list]:
                    if choice == '1':
                        expenses.append(add_expense('expense', budget_lists[choice_list]))
                    elif choice == '2':
                        expenses.append(add_expense('income', budget_lists[choice_list]))

                    save_expense(expenses)
                    break
        # Delete
        elif choice == '3':
            choice = int(input('Enter number: ')) - 1
            choice_del = input(f'Are you sure you want to delete: {expenses[choice]["name"].capitalize()} (y/n): ')
            if choice_del == 'y':
                expenses.pop(choice)
                
                save_expense(expenses)
        # Change name
        elif choice == '4':
            choice = int(input('Enter number: ')) - 1
            new_name = input(f'Enter name({expenses[choice]["name"].capitalize()}): ')
            change = {'name': new_name,
                      'amount': f'{expenses[choice]["amount"]}',
                      'type': f'{expenses[choice]["type"]}'}
            expenses.pop(choice)
            expenses.insert(choice, change)
            
            save_expense(expenses)
        # Change amount
        elif choice == '5':
            choice = int(input('Enter number: ')) - 1
            new_amount = input(f'Enter amount({expenses[choice]["amount"]}): ')
            change = {'name': expenses[choice]["name"].capitalize(),
                      'amount': new_amount,
                      'type': f'{expenses[choice]["type"]}'}
            expenses.pop(choice)
            expenses.insert(choice, change)
            
            save_expense(expenses)
        # Sum expenses
        elif choice == '6':
            with open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8') as expenses_json:
                expenses = json.load(expenses_json)
                count = 0
                for expense in expenses:
                    if expense["type"] == 'expense':
                        count += eval(expense["amount"])
            print(f'\nexpenses = {count}\n')
            input()
        # Sum incomes
        elif choice == '7':
            with open(f'Budget_Calculator/{budget_list}', 'r', encoding='utf-8') as expenses_json:
                expenses = json.load(expenses_json)
                count = 0
                for expense in expenses:
                    if expense["type"] == 'income':
                        count += eval(expense["amount"])
            print(f'\nincomes = {count * -1}\n')
            input()
        # Back
        elif choice == '8':
            budget_list = None
        # Exit
        elif choice == '9':
            break
        else:
            print('Invalid choice. Please select a number between 1 and 6.')
    continue
