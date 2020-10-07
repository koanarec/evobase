import matplotlib.pyplot as plt
import copy
import random
import keyboard
import ast


# This function takes a string representation of a list and then finds all of the elements that have not been calculated
# for example; "1+1" will turn into 2. It returns a list
def fix_list(list_to_fix):
    compiled_string_guts = ""
    cell_of_string_list = copy.deepcopy(list_to_fix)
    cell_of_string_list = cell_of_string_list.split()
    for part_of_string_of_list in cell_of_string_list:
        a_string = str(copy.deepcopy(part_of_string_of_list))
        if a_string[len(a_string) - 2:] == "]]":
            a_string = str(eval(a_string[:len(a_string) - 2])) + "]]"
        elif a_string[len(a_string) - 2:] == "],":
            a_string = str(eval(a_string[:len(a_string) - 2])) + "],"
        elif a_string[0] == "[" and a_string[1] == "[":
            a_string = "[[" + str(eval(a_string[2:len(a_string) - 1])) + ","
        elif a_string[0] == "[" and a_string[len(a_string) - 1] == ",":
            a_string = "[" + str(eval(a_string[1:len(a_string) - 1])) + ","
        else:
            a_string = str(eval(a_string[:len(a_string) - 1])) + ","
        compiled_string_guts = compiled_string_guts + a_string
    return ast.literal_eval(compiled_string_guts)


# This class holds the each formula to calculate the perimeter and mess about with it
class Creature:
    def __init__(self, guts):
        self.__guts = guts

    def return_fitness(self):
        # To change what the program will do take the matrix, self.__guts and make it return an integer for how "fit"
        # it is

        guts = self.__guts
        tot = 0
        for x in guts:
            for a in x:
                tot= tot + a
        return tot

    def __lt__(self, other):
        return self.return_fitness() > other.return_fitness()

    def evolve(self):
        saves = open("temp.txt", "w")
        saves.write(str(creatures[0].return_guts()))
        saves.close()

        a = open('temp.txt', 'r')
        creatures_guts = a.readline()
        srr = ""
        lcv = 0
        for node_in_creatures_guts in creatures_guts:
            factor_of_node_change = int(random.randint(-1, 1))
            if node_in_creatures_guts in "0123456789" and random.randint(0, 100) > 99 and factor_of_node_change != 0:
                origonal = int(creatures_guts[lcv])
                news = int(factor_of_node_change + origonal)
                z = str(news)

                srr = srr + z

            else:

                z = str(creatures_guts[lcv])
                if len(z) > 1:
                    print(z)
                srr = srr + z

            lcv = lcv + 1
        try:
            self.__guts = copy.deepcopy(ast.literal_eval(srr))
        except:
            try:
                self.__guts = copy.deepcopy(fix_list(srr))
            except:
                print("failed to update guts", str(srr))
        a.close()

    def __str__(self):
        return str(self.return_fitness())

    def __int__(self):
        return int(self.return_fitness())

    def return_guts(self):
        return str(self.__guts)


def print_graph(creatures):
    all_stengths = 0
    for creature in creatures:
        all_stengths = all_stengths + creature.return_fitness()
    all_stengths = all_stengths // len(creatures)

    av_vals.append(all_stengths)
    max_vals.append(creatures[0].return_fitness())
    best_cre_fitscore = (creatures[0].return_fitness())
    min_vals.append(creatures[len(creatures) - 1].return_fitness())

    plt.plot(max_vals)
    plt.title(str(best_cre_fitscore))
    # plt.plot(min_vals)
    # plt.plot(av_vals)

    plt.draw()
    plt.pause(0.00001)
    plt.clf()


# This initalizes the loop and imports the best creature from before, it will generate new creatures if it cannot
# import the old ones
number_of_creatures = 16
try:
    a = open('peri.txt', 'r')
    cre_for_poplation_generation = a.readline()
    cre_for_poplation_generation = ast.literal_eval(cre_for_poplation_generation)
    a.close()
except:
    # 8 = 69
    creatures_guts_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cre_for_poplation_generation = []
    for x in creatures_guts_row:
        cre_for_poplation_generation.append(creatures_guts_row)

creatures = []

lcv = 32

while lcv > 0:
    lcv = lcv - 1
    creatures.append(Creature(cre_for_poplation_generation))



max_vals = []
min_vals = []
av_vals = []
lcv = 0
while lcv < 10000000000000:
    lcv = lcv + 1
    creatures.sort()

    # This saves the best animal in a text file
    save = open("peri.txt", "w")
    save.write(str(creatures[0].return_guts()))
    save.close()

    print_graph(creatures)


    # This isn't very good. It chooses which creatures to kill, evolve and replicate
    best_quater = copy.deepcopy(creatures[:len(creatures) // 4])
    upper_quartile = copy.deepcopy(creatures[len(creatures) // 4:(len(creatures) // 4) * 2])
    creatures.clear()
    del creatures[:]
    creatures = []
    for x in best_quater:
        creatures.append(x)
        temp = copy.deepcopy(x)
        temp.evolve()
        creatures.append(temp)
    for x in upper_quartile:
        creatures.append(x)
        temp = copy.deepcopy(x)
        temp.evolve()
        creatures.append(temp)

    # This can reset the graph that you look at just to help read changes
    if keyboard.is_pressed('q'):
        max_vals = []
        min_vals = []
        av_vals = []
