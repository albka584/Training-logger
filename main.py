from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

# fel på exercise counten
# fel om man lägger till flera sets på en och samma dag
# går ej plotta graf om man bara har 1 övning, ska ej gå då!

class Traininglog:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

#idag, fixa add sets loopen
# fixa sort data, och self.count_exercsises_today

    def add_excersise_gym(self, name, sets, date):
        i = self.count_exercises_today() # skriva self. för att få tag på funk
        exercise = {'name' : name, 'sets' : sets, 'date' : date, 'Exercsise count: ': i}

        for item in self.data:
            last_set = item['sets'][-1][2]
            if date == item["date"] and name == item["name"]:
                last_set += 1
                s = exercise['sets']

                s[2] = last_set
                item['sets'].extend([s])
                break 
        else: 
            self.data.append(exercise)
        self.save_data()
    
    def sort_dates(self, data):
        sort_dates = sorted(data, key=lambda date: datetime.strptime(date["date"], "%d/%m/%y"))
        return sort_dates

    def show_exercise(self, data):
        sort_date = self.sort_dates(data)
        for i in sort_date:
            print(i)

    def save_data(self):
        if self.data:
            with open(self.filename, 'w') as f:
                for item in self.data:
                    json.dump(item,f)
                    f.write('\n')

    def count_exercises_today(self): # vrf inte denna fungera ???
        with open(self.filename, 'r') as f: # läser in allt som en sträng, inte dictionary. därav konvertera? Json sträng?
            i=1
            for row in f:
                exercise = json.loads(row) # rstrip behövs ? tar bort spaces. loads() konverterar sträng till dict
                if (exercise["date"]) == datetime.today().strftime("%d/%m/%y"):
                    i+=1
            return i 
        
    def remove_exercies(self,num, date): # bör kör with open här, för att öppna alla filerna, och sedan tag fram indexet korrekt
        with open(self.filename, 'r') as g:
            lines = g.readlines()

        new_file=[]
        for line in lines:
            rows = json.loads(line)
            if (rows["Exercsise count: "] != num or date != rows["date"]): # vad blir skillnad mellan or & and?
                new_file.append(json.dumps(rows) + '\n') # blev tomt utan json.dumps
        
        with open(self.filename, 'w') as f:
            f.writelines(new_file)

    def load_data(self):
        exercsises=[]
        with open(self.filename, 'r') as f:
            for i in f:
                exercsises.append(json.loads(i))
        return exercsises

    def plot_tot_weight(self, date_idx1, date_idx2, data):
        weight=[]
        dates=[]
        for i in range(date_idx1-1, date_idx2):
            sets = data[i]["sets"]
            dates.append(data[i]["date"])
            c = 0
            for j in sets:
                c += j[0]*j[1]
            weight.append(c)
        plt.figure(figsize=(10,5))
        plt.plot(dates, weight, marker='o', linestyle='-', color='b')
        plt.title(f'Totalvikt över tid, {data[0]["name"]}')
        plt.xlabel('Datum')
        plt.ylabel('Totalvikt')
        plt.show()

    def plot_max_reps(self, date_idx1, date_idx2, num_reps, data):
        weight_date = {}
        for i in range(date_idx1-1, date_idx2):            
            date = data[i]["date"]
            if date not in weight_date:
                weight_date[date] = []
            for j in range(len(data[i]["sets"])):
                weight = data[i]["sets"][j][0]
                reps = data[i]["sets"][j][1]
                if reps == num_reps:
                    weight_date[date].append(weight)
        dates=[]
        weights=[]
        for date,weight in weight_date.items():
            if len(weight_date[date]) != 0:
                dates.append(date) 
                weights.append(max(weight))

        if all(len(weight) == 0 for weight in weight_date.values()):
            print('Fanns ingen data tillgänglig')
            return 0

        plt.figure(figsize=(10,5))
        plt.plot(dates, weights, marker='o', linestyle='-', color='b')
        plt.title(f'Maxvikt över tid, {data[0]["name"]}, antal reps: {num_reps}')
        plt.xlabel('Datum')
        plt.ylabel('Maxvikt')
        plt.show()

Training_log = Traininglog('training_log.txt')

def main_menu():
    print("Huvudmeny:")
    print("1. Lägg till övning")
    print("2. Visa alla övningar")
    print("3. Radera en övning")
    print("4. Plotta graf")
    #print('ta bort övning')
    #print('lägg till vikter på övning')
    #print('redigera övning')
    print("Tryck quit för att avsluta\n")

def add_sets():
    num_set=0
    sets=[]

    while True:
        #os.system('cls')
        print('Lägg till ett set: Y/N')
        answer = input()
        if answer == 'n'.lower():
            os.system('cls')
            break
        if answer == 'y'.lower():
            try:
                os.system('cls')
                print("Vilken vikt?")
                weight = int(input())
                print("Antal reps?")
                reps = int(input())
                num_set+=1 
                sets.append([weight, reps, num_set])
                print(sets)
            except:
                print("\n *****Sets eller reps bör vara ints***** \n") 
            #os.system('cls')
    return sets, num_set

#lägga in så man kan köra back eller quit överallt

while True:
    main_menu()
    command = input()

    if command.lower() == "quit":
        break
    
    if command == "1":
        os.system('cls')
        print("1. Lägg till en övning") # fixa så man kan lägga in datum också
        print("2. Välj datum.")
        today = datetime.today().strftime("%d/%m/%y")
        
        new_command = input()
        if new_command == '1':
            os.system('cls')
            name = input('Övningens namn? ')
            sets, num_set = add_sets()
            if sets:
                Training_log.add_excersise_gym(name, sets, today)
        if new_command == '2': # date_ == datetime.strptime(date_, "%d/%m/%y") 
            os.system('cls')
            print('[Enter: dagens datum] [mm/dd/yy]')
            date_ = input("Välj datum: ")
            try:
                if date_ == '':
                    date_ = today
                    name = input("Övningens namn? ")
                    sets, num_set = add_sets()
                    Training_log.add_excersise_gym(name, sets, date_)
                elif date_ == datetime.strptime(date_, "%d/%m/%y").strftime("%d/%m/%y"): # raisar exception, strptime
                    name = input("Övningens namn? ")
                    sets, num_set = add_sets()
                    Training_log.add_excersise_gym(name, sets, date_)
            except:
                print ( ' **** Fel format på datum. Format: [mm/dd/yy] eller tryck Enter ****  \n')
                    
    if command == '2':
        os.system('cls')
        Training_log.show_exercise(Training_log.data) # välj datum
    if command == '3':
        #os.system('cls')
        print("Välj vilken övning du vill radera [nr] och datum [dd/mm/yy]")
        Training_log.show_exercise(Training_log.data)
        num_date = input()
        num_date = num_date.split()
        if len(num_date) == 2:
            number = int(num_date[0])
            date_ = num_date[1]
        else:
            #os.system('cls')
            continue
        Training_log.remove_exercies(number, date_)
        
    if command == '4':
        os.system('cls')
        while True:
            name_exercsise = input("Välj övning: ")
            data_log=[]
            found = False
            sort_data = Training_log.sort_dates(Training_log.data)
            for i in sort_data:
                if i["name"] == name_exercsise:
                    data_log.append(i)
                    found = True
            if found:
                break
            else:
                os.system('cls')
                print('Ange en övning som finns')
                continue
            
        os.system('cls')
        while True:
            indx=[]
            for idx,item in enumerate(data_log, start=1):
                indx.append(idx)
                print(f"{idx}. {item['date']}")
            dates = input("[nr1 nr2]. Välj mellan vilka datum: ")
            dates_idx = dates.split()

            if len(dates_idx) == 2:
                #try:
                    dates_idx0 = int(dates_idx[0])
                    dates_idx1 = int(dates_idx[1])
                    if int(dates_idx0) >= indx[0] and int(dates_idx1) <= indx[-1]:
                        while True:
                            print("1. Välj totalvikt")
                            print("2. Välj maxvikt för antalet reps")
                            command = input()
                            if command == '1':
                                Training_log.plot_tot_weight(dates_idx0, dates_idx1, data_log)
                                break
                            elif command == '2':
                                chose_num_reps = int(input("Välj antal reps: "))
                                Training_log.plot_max_reps(dates_idx0, dates_idx1, chose_num_reps, data_log)
                                break
                        break
                    else:
                        os.system('cls')
                        print("Dessa datum finns ej. Försök igen ")
                #except:
                    print('Fel format. Försök igen ')
                    continue
            else:
                print ('Fel format. Försök igen ')
            
    if command == '5':
        add_sets()

# för varje set, göra en lista, som innehåller vikt
# excersises, 
# istället för antalet set, så lägger man till övning, med tillhörande reps / sets

