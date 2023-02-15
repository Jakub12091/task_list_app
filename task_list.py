import pickle 
from datetime import datetime
from datetime import timedelta
import time

class Task:
    def __init__(self, creation_date, priority, desc, deadline ):
        self.creation_date = creation_date
        self.priority = priority
        self.desc = desc
        self.deadline = deadline

    def __str__(self):
        return f'Priority: {self.priority}\nCreaton date: {datetime.strftime(self.creation_date,"%Y-%m-%d")}\n\
            \rDescription: {self.desc}\nDeadline: {datetime.strftime(self.deadline,"%Y-%m-%d")}'


class ToDoList:
    """Class ToDoList contains list in which tasks are stored while using program. 
    This class also contains all the methods enabling adding new tasks, deleting them,
    displaying list and launching menu.
    List of tasks is loaded from the pickle file by load_list method.
    load_list will create empty pickle file if there is none in the given path.
    dump_and_quit method saves tasks into a pickle file and quits program."""

    list = []
    path = ""

    def load_list(self):
        print('The task list is saved and load from a pickle file\n\
        \rEnter the path to your to-do list if you have used this application before\n\
        \rIf else, specify the path where the pickle file is to be stored (for example C:/Users/Tom/mylist.pcl)')

        while True:
            try:
                self.path = input()
                if self.path[-3:] != "pcl":
                    print('Given path does not end with pcl extension, insert path ending with "filename.pcl"') 
                else:
                    with open(self.path,'a+b') as f:
                        print('Path absorbed, file is ready')
                        break

            except FileNotFoundError:
                print('The path does not exist, paste the correct path')

            except PermissionError: 
                print('Permission denied. Is the path you provided simply C:/Users/mylist.pcl ?\n\
                \rTry providing deeper path, like C:/Users/Tom/mylist.pcl\n')

            except:
                print('Unknown problem occurred, please try again using different path')

        try:
            with open(self.path,'r+b') as f:
                self.list = pickle.load(f)
                print('Tasks from the file absorbed')
        except:
            print("No tasks absorbed from the file. Let's create some tasks")

        time.sleep(1)
        self.menu()


    def add_task(self):
        while True:
            priority = str(input('Set task priority to high? (Y/N)\n'))     

            if priority != "Y" and priority != "N":
                print('Wrong value. Press Y for high priority, N for normal priority')

            else:
                if priority == "Y":
                    priority = "High"
                else:
                    priority = "Normal"
                break

        desc = input('Describe the task in few words\n')

        while True:
            deadline = input('Set the deadline, use format YYYY-MM-DD\n')
            try:
                deadline = datetime.strptime(deadline,"%Y-%m-%d")
            except:
                print("An error occurred, did you follow the YYYY-MM-DD format? Try again")
            else:
                break
        
        creation_date = datetime.now()

        #high priority task are placed first on the list
        if priority == "High":
            self.list = [Task(creation_date, priority, desc, deadline)] + self.list

        else:
            self.list.append(Task(creation_date, priority, desc, deadline))

        print('Task successfully added to list')
        time.sleep(1)
        self.menu()


    def delete_task(self):
        if len(self.list) == 0:
            print("There are no tasks in your list yet, let's come back to menu")
            time.sleep(2)
            self.menu()

        elif len(self.list) == 1:
            print(f'There is only one task in your list:\n{self.list[0]}\n')

            while True:
                delete_choice = str(input('Delete the task? (Y/N)\n'))

                if delete_choice != "Y" and delete_choice != "N":
                    print('Wrong value, try again')

                elif delete_choice == "Y":
                    del self.list[0]
                    print('Task successfully removed')
                    time.sleep(1)
                    self.menu()

                else:
                    print('Coming back to menu...')
                    time.sleep(1)
                    self.menu()

        else:
            print('Below you will see the list, input the number of the task that should be removed')
            time.sleep(2)

            for index, item in enumerate(self.list):
                print(f'\nTask number:{index + 1}\n{item}')
            
            while True:
                try:
                    delete_choice = input('\nWhich task to remove?\n\
                    \rIf you changed your mind we can come back to menu, just press "M" instead\n')

                    if delete_choice == "M":
                        break

                    else:
                        delete_choice = int(delete_choice)
                        del self.list[delete_choice - 1]

                except:
                    print('Did you input an integer value? Please input the number of the task\n\
                    \rthat should be removed')

                else:
                    print('Task successfully removed')
                    break

            print('Coming back to menu...')
            time.sleep(2)
            self.menu()


    def display_list(self):
        if len(self.list) == 0:
            print("There are no tasks in your list yet, let's come back to menu")
            time.sleep(2)
            self.menu()

        print('Below you will see every task currently stored in your ToDoList:')
        time.sleep(1)

        for task in self.list:
            days_to_deadline = (task.deadline - task.creation_date) + timedelta(days=1) 

            if days_to_deadline.days < 0:
                print(f'\n{task}\nDays past deadline: {(days_to_deadline.days)*-1}!')

            elif days_to_deadline.days == 0:
                print(f'\n{task}\nToday is the deadline!')

            else:
                print(f'\n{task}\nDays till deadline: {days_to_deadline.days}')

        self.menu()

    def dump_and_quit(self):
        print('Saving list to a pickle file... Bye!')
        time.sleep(1)
        with open(self.path,'wb') as f:
            pickle.dump(self.list, f)
        quit()


    def menu(self):
        while True:
            try:
                menu_choice = int(input('\nWhat do we do?\nPress 1 to add new task\n\
                \rPress 2 to remove one of the tasks from the list\n\
                \rPress 3 to display the list\nPress 4 to quit\n'))

            except ValueError:
                print('Wrong value, press 1, 2, 3 or 4')
            
            else:
                if menu_choice > 4 or menu_choice < 1:
                    print('Wrong value, press 1, 2, 3 or 4')
                else:
                    break

        if menu_choice == 1:
            self.add_task()
        elif menu_choice == 2:
            self.delete_task()
        elif menu_choice == 3:
            self.display_list()
        else:
            self.dump_and_quit()

new_list = ToDoList()
new_list.load_list()
