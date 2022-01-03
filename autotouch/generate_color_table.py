#takes a 5x5 matrix of pixel colors extracted from idol portraits, and outputs a color table for 5,3,2 idols 
#and any other supplementary information 
from itertools import permutations
import copy

m = [
[6248317, 11958115, 6241581, 5398945, 16772778],
[15854809, 6578308, 12813157, 10054225, 4014977],
[5002893, 12397618, 7236250, 13539966, 12485217],
[10053459, 7239106, 15124625, 10385275, 15317913],
[16640210, 9723982, 5136285, 16088676, 9662331]
]

def printColorTables(m: 'list[list[int]]'):
    #assert m is 5x5 matrix of int
    assert(len(m)==5 and len(m[0])==5), 'matrix has incorrect dimensions' 
    
    #convert int to str 
    for i in m:
        for j in i:
            m[m.index(i)][i.index(j)] = str(m[m.index(i)][i.index(j)])

    #sort pixels by idol
    idolSortedM = [
        [],
        [],
        [],
        [],
        []
    ]

    currentIndex = 0
    for i in range(5):
        for j in range(5):
            idolSortedM[i].append(m[currentIndex][j])
            if j != 4:
                if currentIndex == 4:
                    currentIndex = 0
                else:
                    currentIndex += 1

    m = copy.deepcopy(idolSortedM)
    print(m)

    #generate idol order lists for 5,3,2
    perm = permutations(['0','1','2','3','4'])
    order5 = []
    order3 = []
    order2 = [] 

    for i in list(perm):
        order5.append(i)

        in3 = False
        for j in order3:
            if i[1] + i[2] + i[3] == j[1] + j[2] + j[3]:
                in3 = True

        if in3 == False:
            order3.append(i)
        
        in2 = False
        for k in order2:
            if i[1] + i[2] == k[1] + k[2]:
                in2 = True

        if in2 == False:
            order2.append(i)

    assert(len(order5)==120 and len(order3)==60 and len(order2)==20), f"length of order lists unexpected, {len(order5)} {len(order3)} {len(order2)}"

    #generate tables for 5,3,2 idols
    def fillTable(orders) -> list:
        table = []
        for order in orders:
            s = ''
            for i in range(len(orders[0])):
                s += m[int(order[i])][i]
            table.append(s)
        return table

    table5 = fillTable(order5)
    table3 = fillTable(order3)
    table2 = fillTable(order2)

    #print tables in convenient format for copy pasting into lua scripts
    def tablePrint(table):
        for s in table:
            if table.index(s) != len(table)-1:
                print(f"'{s}',")
            else:
                print(f"'{s}'")
        return None 

    print('\ntable5:\n')
    tablePrint(table5)

    print('\ntable3:\n')
    tablePrint(table3)

    print('\ntable2:\n')
    tablePrint(table2)

    return None

if __name__ == "__main__":
    printColorTables(m)
