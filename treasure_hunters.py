import os
import random
from time import *

rules = "Правила:\n1. Ход выполняется клавишами \"w\"(вверх), \"s\"(вниз), \"a\"(влево), \"d\"(вправо).\n" \
        "2. Если не удается сделать шаг, значит на пути стена и нужно к букве хода добаить букву \" e\" - она удалит " \
        "стену. На всю игру игроку доступны три кирки. После использования букву \" e\" количество кирок уменьшается " \
        "на одну.\n" \
        "3. Если игрок попал в яму, то он затем он оказывается на выходе другой, связанной с ней.\n" \
        "4. Если вместо буквы хода использовкать букву \" i\", то сможете увидеть сколько у вас кирок и сколько всего " \
        "ходов вы сделали.\n" \
        "5. Необходимо найти клад и принести его к выходу.\n"

# Players
player = {"x1": 1, "y1": 1, "content": "", "visible": 1, "pickaxe": 3, "moves": 0}

# Field size
n = 10


# Generate cell for field
def generate_cell(x, y):
    cell = {"x1": x, "y1": y, "content": "I", "visible": 0, "walls": " "}
    i = 0

    while i < 2:
        cell.update({"walls": random.choice([" ", "I"])})
        i += 1

    if x == 0:
        cell.update({"walls": "I"})
    elif x == 9:
        cell.update({"walls": "I"})
    elif y == 0:
        cell.update({"walls": "I"})
    elif y == 9:
        cell.update({"walls": "I"})

    return cell


# Generate (x, y)
def random_for_xy():
    x = random.choice([2, 3, 4, 5, 6, 7, 8])
    y = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
    return [x, y]


# Print field with others
def print_field(field):
    for row in field:
        for _ in row:
            if _.get("x1") == player.get("x1") and _.get("y1") == player.get("y1"):
                _.update({"walls": " ", "content": "P", "visible": 1})
                print("%2s" % "P", end=" ")
            elif _.get("x1") == hole_one.get("x1") and _.get("y1") == hole_one.get("y1"):
                _.update({"walls": " ", "content": "H1"})
                if _.get("visible") == 0:
                    print("%2s" % "I", end=" ")
                elif _.get("visible") == 1:
                    print("%2s" % "H", end=" ")
            elif _.get("x1") == hole_two.get("x1") and _.get("y1") == hole_two.get("y1"):
                _.update({"walls": " ", "content": "H2"})
                if _.get("visible") == 0:
                    print("%2s" % "I", end=" ")
                elif _.get("visible") == 1:
                    print("%2s" % "H", end=" ")
            elif _.get("x1") == treasure.get("x1") and _.get("y1") == treasure.get("y1"):
                _.update({"walls": " ", "content": "$"})
                if _.get("visible") == 0:
                    print("%2s" % "I", end=" ")
                elif _.get("visible") == 1:
                    print("%2s" % "$", end=" ")
            else:
                if _.get("visible") == 0:
                    print("%2s" % "I", end=" ")
                elif _.get("visible") == 1:
                    print("%2s" % _.get("walls"), end=" ")
        print()


# Print field after win
def print_field_after_win(field):
    for row in field:
        for _ in row:
            if _.get("x1") == player.get("x1") and _.get("y1") == player.get("y1"):
                _.update({"walls": " ", "content": "P"})
                print("%2s" % "P", end=" ")
            elif _.get("x1") == hole_one.get("x1") and _.get("y1") == hole_one.get("y1"):
                _.update({"walls": " ", "content": "H1"})
                print("%2s" % "H", end=" ")
            elif _.get("x1") == hole_two.get("x1") and _.get("y1") == hole_two.get("y1"):
                _.update({"walls": " ", "content": "H2"})
                print("%2s" % "H", end=" ")
            elif _.get("x1") == treasure.get("x1") and _.get("y1") == treasure.get("y1"):
                _.update({"walls": " ", "content": "$"})
                print("%2s" % "$", end=" ")
            else:
                print("%2s" % _.get("walls"), end=" ")
        print()


# Control players steps

def player_step(st):
    tmpx = player.get("x1")
    tmpy = player.get("y1")
    p = ""
    if st == "a" and player.get("y1") > 1 and field[tmpx][tmpy - 1].get("walls") == " ":
        p = {"y1": player.get("y1") - 1, "moves": player.get("moves") + 1}
        field[tmpx][tmpy - 1].update({"visible": 1})
    elif st == "a" and player.get("y1") >= 2 and field[tmpx][tmpy - 1].get("walls") == " ":
        p = {"y1": player.get("y1") - 1, "moves": player.get("moves") + 1}
        field[tmpx][tmpy - 1].update({"visible": 1})
    elif (st == "ea" or st == "ae") and player.get("y1") >= 2 and field[tmpx][tmpy - 1].get("walls") == "I":
        if player.get("pickaxe") > 0:
            p = {"y1": player.get("y1") - 1, "pickaxe": player.get("pickaxe") - 1, "moves": player.get("moves") + 1}
            field[tmpx][tmpy - 1].update({"walls": " ", "visible": 1})
        else:
            print("Количество кирок: " + str(player.get("pickaxe")) + "\n" + "Вам нечем ломать стену.\n")
    elif st == "d" and player.get("y1") <= 7 and field[tmpx][tmpy + 1].get("walls") == " ":
        p = {"y1": player.get("y1") + 1, "moves": player.get("moves") + 1}
        field[tmpx][tmpy + 1].update({"visible": 1})
    elif (st == "ed" or st == "de") and player.get("y1") <= 7 and field[tmpx][tmpy + 1].get("walls") == "I":
        if player.get("pickaxe") > 0:
            p = {"y1": player.get("y1") + 1, "pickaxe": player.get("pickaxe") - 1, "moves": player.get("moves") + 1}
            field[tmpx][tmpy + 1].update({"walls": " ", "visible": 1})
        else:
            print("Количество кирок: " + str(player.get("pickaxe")) + "\n" + "Вам нечем ломать стену.\n")
    elif st == "w" and player.get("x1") > 1 and field[tmpx - 1][tmpy].get("walls") == " ":
        p = {"x1": player.get("x1") - 1, "moves": player.get("moves") + 1}
        field[tmpx - 1][tmpy].update({"visible": 1})
    elif st == "w" and player.get("x1") >= 2 and field[tmpx - 1][tmpy].get("walls") == " ":
        p = {"x1": player.get("x1") - 1, "moves": player.get("moves") + 1}
        field[tmpx - 1][tmpy].update({"visible": 1})
    elif (st == "ew" or st == "we") and player.get("x1") >= 2 and field[tmpx - 1][tmpy].get("walls") == "I":
        if player.get("pickaxe") > 0:
            p = {"x1": player.get("x1") - 1, "pickaxe": player.get("pickaxe") - 1, "moves": player.get("moves") + 1}
            field[tmpx - 1][tmpy].update({"walls": " ", "visible": 1})
        else:
            print("Количество кирок: " + str(player.get("pickaxe")) + "\n" + "Вам нечем ломать стену.\n")
    elif st == "s" and player.get("x1") <= 7 and field[tmpx + 1][tmpy].get("walls") == " ":
        p = {"x1": player.get("x1") + 1, "moves": player.get("moves") + 1}
        field[tmpx + 1][tmpy].update({"visible": 1})
    elif (st == "es" or st == "se") and player.get("x1") <= 7 and field[tmpx + 1][tmpy].get("walls") == "I":
        if player.get("pickaxe") > 0:
            p = {"x1": player.get("x1") + 1, "pickaxe": player.get("pickaxe") - 1, "moves": player.get("moves") + 1}
            field[tmpx + 1][tmpy].update({"walls": " ", "visible": 1})
        else:
            print("Количество кирок: " + str(player.get("pickaxe")) + "\n" + "Вам нечем ломать стену.\n")
    else:
        pass
    return p


# Clear field from the walls
def clear_field():
    for row in field:
        # print("row[0] =", row[0])
        for i in range(1, 6):
            if row[i].get("walls") == " " and row[i + 1].get("walls") == "I" and row[i + 2].get("walls") == " ":
                row[i + 1].update({"walls": " "})
            elif row[i].get("walls") == "I" and row[i + 1].get("walls") == "I" and row[i + 2].get("walls") == " ":
                row[i].update({"walls": " "})


# Player and hole
def player_and_hole(x, y):
    if hole_one.get("x1") == x and hole_one.get("y1") == y:
        player.update({"x1": hole_one.get("x2"), "y1": hole_one.get("y2")})
        field[x][y].update({"visible": 1})
    elif hole_two.get("x1") == x and hole_two.get("y1") == y:
        player.update({"x1": hole_two.get("x2"), "y1": hole_two.get("y2")})
        field[x][y].update({"visible": 1})


# Player and treasure
def player_and_treasure():
    if treasure.get("x1") == player.get("x1") and treasure.get("y1") == player.get("y1"):
        player.update({"content": "$"})
        print("$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $")
        print("$ Клад найден! Несите его к выходу. $")
        print("$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $\n")
        treasure.clear()
    else:
        pass


# Player win or not
def player_win():
    if player.get("x1") == 1 and player.get("y1") == 1 and player.get("content") == "$":
        print("Ура!!! Победа!!!")
        return "q"
    else:
        pass


# Generate field size n
field = list()
for i in range(n):
    field.append([])
    for j in range(n):
        field[i].append(generate_cell(i, j))


# Clear terminal
def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')


clear_field()

# Generate hole
xy1 = random_for_xy()
xy2 = random_for_xy()

hole_one = {"x1": xy1[0], "y1": xy1[1], "content": "", "visible": 0, "x2": xy2[0], "y2": xy2[1]}
hole_two = {"x1": xy2[0], "y1": xy2[1], "content": "", "visible": 0, "x2": xy1[0], "y2": xy1[1]}

# Generate treasure
xy3 = random_for_xy()

treasure = {"x1": xy3[0], "y1": xy3[1]}

print(rules)
print_field(field)
print()
step = input("Сделайте ход!" + "\n")
while step != "q":
    clear()
    # print(rules)
    print()
    player.update(player_step(step))
    player_and_hole(player.get("x1"), player.get("y1"))
    player_and_treasure()
    print_field(field)
    print()

    if step == "i":
        if player.get("content") != "$":
            print("Клад не найден." + "\n" + "Количество кирок: " + str(
                player.get("pickaxe")) + "\n" + "Вы сделали " + str(player.get("moves")) + " шагов.")
        elif player.get("content") == "$":
            print("Клад у вас." + "\n" + "Количество кирок: " + str(
                player.get("pickaxe")) + "\n" + "Вы сделали " + str(player.get("moves")) + " шагов.")
    print()

    if player_win() == "q":
        print()
        print_field_after_win(field)
        step = "q"
    else:
        step = input("Сделай шаг!" + "\n")

sleep(100)
