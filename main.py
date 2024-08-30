from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

class Traininglog:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.sort_dates()

    def add_exercise_gym(self, name, sets, date):
        exercise = {'name' : name, 'sets' : sets, 'date' : date}

        for item in self.data:
            last_set = item['sets'][-1][2]
            if date == item["date"] and name == item["name"]:
                for i in sets:
                    last_set+=1
                    i[2] = last_set
                    item['sets'].extend([i])    
                break 
        else: 
            self.data.append(exercise)
        self.save_data()
    
    def sort_dates(self):
        self.data = sorted(self.data, key=lambda date: datetime.strptime(date["date"], "%d/%m/%y"))
        return self.data
    
    def show_set(self, data):
        for j in data['sets']:
            print(f"set: {j[2]}, weight: {j[0]} kgs, reps: {j[1]}")

    def show_exercise(self): # här kan vi också ha en jävla massa val. vilken dag osv man vill kika
        for i in self.data:
            for j in i['sets']:
                print(f"{i['date']}, {i['name']}, set: {j[2]}, weight: {j[0]} kgs, reps: {j[1]}")

    def save_data(self):
        if self.data:
            with open(self.filename, 'w') as f:
                for item in self.data:
                    json.dump(item,f)
                    f.write('\n')

        
    def remove_exercise(self,date_idx): # kanske går att göra denna mkt enklare?
        with open(self.filename, 'r') as g:
            lines = g.readlines()

        new_file=[]
        date_idx-=1
        remove_data = self.data[date_idx]
        for line in lines:
            rows = json.loads(line)
            if rows["date"] != remove_data["date"] or rows["name"] != remove_data["name"]: # and måste båda villkoren vara sanna
                new_file.append(json.dumps(rows)+'\n')
        
        with open(self.filename, 'w') as f:
            f.writelines(new_file)
        self.data.pop(date_idx) 

    def remove_set(self, chosen_exercise, remove_idx, date_idx):
        sets=[]
        for i in chosen_exercise['sets']:
            if i[2] != remove_idx:
                sets.append(i)
        chosen_exercise['sets'] = sets
        self.save_data()

        if not chosen_exercise['sets']:
            self.remove_exercise(date_idx)

        for idx,item in enumerate(chosen_exercise['sets'], start=1):
            item[2] = idx
        self.save_data()

    def load_data(self):
        exercise=[]
        with open(self.filename, 'r') as f:
            for i in f:
                exercise.append(json.loads(i))
        return exercise

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
    print("3. Radera")
    print("4. Plotta")
    print('5. Redigera övning')
    print("Tryck quit för att avsluta\n")

def add_sets():
    num_set=0
    while True:
        os.system('cls')
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
            except:
                print("\n *****Sets eller reps bör vara ints***** \n") 
            os.system('cls')
    return sets, num_set

while True:
    unique_names=set()
    for i in Training_log.data:
        unique_names.add(i["name"])

    main_menu()
    command = input()

    if command.lower() == "quit":
        break
    sets=[]
    if command == "1":
        os.system('cls')
        print("1. Idag.") # fixa så man kan lägga in datum också
        print("2. Annat datum.")
        today = datetime.today().strftime("%d/%m/%y")
        command = input()
        if command == '1':
            os.system('cls')
            name = input('Övningens namn? ')
            sets, num_set = add_sets()
            if sets:
                Training_log.add_excersise_gym(name, sets, today)
        elif command == '2':
            os.system('cls')
            print("1. Välj befintlig datum.")
            print("2. Välj nytt datum.")
            command = input()
            if command == '1':
                dates = list(i["date"] for i in Training_log.data)
                unique_dates = list(dict.fromkeys(dates)) # gör om till en dict. inga dubbletter i en dict

                for date_idx, date in enumerate(unique_dates,start=1):
                    print(f"{date_idx}. {date}")
                    
                date_num = int(input())
                name = input("Övningens namn? ")

                sets, num_set = add_sets()
                Training_log.add_exercise_gym(name, sets, unique_dates[date_num-1])

            elif command == '2':
                print('dd/mm/yy')
                date = input("Välj datum: ") # typ få en lista med 
                try:
                    if date == datetime.strptime(date, "%d/%m/%y").strftime("%d/%m/%y"):
                        name = input("Övningens namn? ")
                        sets, num_set = add_sets()
                        Training_log.add_exercise_gym(name, sets, date)
                except:
                    print ( ' **** Fel format på datum. Format: mm/dd/yy ****  \n')
                    
    elif command == '2':
        os.system('cls')
        Training_log.show_exercise() 
    if command == '3':
        #os.system('cls')
        print(unique_names)
        name = input("Välj övning: ") 
        for idx,item in enumerate(Training_log.data, start=1):
            if item["name"] == name:
                print(f"{idx}. {item['date']}") # jag behöver motsvarande idx för hela datasetet
        try:
            dates_num = int(input("Välj ett datum: "))
        except:
            continue
        print("1. Ta bort ett set")
        print("2. Ta bort hela övningen")
        command = input()
        if command == '1':
            chosen_exercise = Training_log.data[dates_num-1]
            Training_log.show_set(chosen_exercise)
            remove_idx = int(input("Välj vilket set du vill ta bort: "))
            Training_log.remove_set(chosen_exercise, remove_idx, dates_num)

        if command == '2':
            Training_log.remove_exercise(dates_num) # fixa så den kan tag bort liksom flera övningar samtidigt
        
    if command == '4':
        os.system('cls')
        while True:
            print(unique_names)
            name_exercise = input("Välj övning: ")
            data_log=[]
            found = False
            for i in Training_log.data:
                if i["name"] == name_exercise:
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
            dates = input("[nr1 nr2]. Välj mellan vilka datum: ") # om längden av dates<2, stop
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
        pass


# hantera lite fel fall
# fixa back knapp och quit närsom?
# lägg till löpning?