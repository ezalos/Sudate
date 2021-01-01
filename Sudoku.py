import argparse
import copy

class Sudoku:
    def __init__(self, sudoku=None, pos=None):
        if sudoku == None:
            self.sudoku = [ [0] * 9 ] * 9
        else:
            self.sudoku = copy.deepcopy(sudoku)
        if pos == None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        print(self)

    def next_pos(self):
        n_pos = copy.deepcopy(self.pos)
        n_pos[1] += 1
        if n_pos[1] > 8:
            n_pos[1] = 0
            n_pos[0] += 1
            if n_pos[0] > 8:
                return None
        return n_pos

    def solve(self):
        print(self)
        n_pos = self.next_pos()
        if n_pos == None:
            if self.sudoku[self.pos[0]][self.pos[1]] == 0:
                for c in range(1, 10):
                    self.sudoku[self.pos[0]][self.pos[1]] = c
                    print(self)
                    if self.check_line() and self.check_group():
                        break
                    else:
                        self.sudoku[self.pos[0]][self.pos[1]] = 0
                if self.sudoku[self.pos[0]][self.pos[1]] == 0:
                    return None
            return self
        if self.sudoku[self.pos[0]][self.pos[1]] == 0:
            for c in range(1, 10):
                self.sudoku[self.pos[0]][self.pos[1]] = c
                print(self)
                if self.check_line() and self.check_group():
                    n = Sudoku(self.sudoku, n_pos)
                    res = n.solve()
                    if res != None:
                        return res
                self.sudoku[self.pos[0]][self.pos[1]] = 0
        else:
            n = Sudoku(self.sudoku, n_pos)
            res = n.solve()
            if res != None:
                return res
        return None

    def check_line(self):
        pos = self.pos
        case = self.sudoku[pos[0]][pos[1]]
        for i in range(9):
            if i != pos[1] and self.sudoku[pos[0]][i] == case:
                return False
        for i in range(9):
            if i != pos[0] and self.sudoku[i][pos[1]] == case:
                return False
        return True

    def check_group(self):
        pos = self.pos
        case = self.sudoku[pos[0]][pos[1]]
        begin_x = int(pos[0] / 3) * 3
        begin_y = int(pos[1] / 3) * 3
        for x in range(3):
            for y in range(3):
                if begin_x + x != pos[0] or begin_y + y != pos[1]:
                    if case == self.sudoku[begin_x + x][begin_y + y]:
                        return False
        return True

    def __str__(self):
        string = ""
        string += "\033[0;0H"
        for x in range(9):
            for y in range(9):
                if self.sudoku[x][y] == 0:
                    string += "\x1b[{};2;{};{};{}m".format(38, 255, 155, 155)
                elif x == y and x <= 3:
                    string += "\x1b[{};2;{};{};{}m".format(38, 55, 255, 255)
                elif x == y and x >= 5:
                    string += "\x1b[{};2;{};{};{}m".format(38, 255, 255, 55)
                elif x == self.pos[0] and y == self.pos[1]:
                    string += "\x1b[{};2;{};{};{}m".format(48, 255, 255, 255)
                else:
                    string += "\x1b[{};2;{};{};{}m".format(38, 255, 255, 255)
                string += str(self.sudoku[x][y])
                string += "\x1b[0m"
                string += " "
                if y % 3 == 2 and y < 8:
                    string += "|" 
                    string += " " 
            string += "\n"
            if x % 3 == 2 and x < 8:
                string += "-" * 11 * 2 
                string += "\n"
        #string += str(self.pos) + "\n"
        return string

def get_base(date_1=None, date_2=None):
    sudoku = [[0 for i in range(10)] for j in range(10)]
    if date_1:
        sudoku[0][0] = int(date_1 / 1000) % 10
        sudoku[1][1] = int(date_1 / 100) % 10
        sudoku[2][2] = int(date_1 / 10) % 10
        sudoku[3][3] = int(date_1 / 1) % 10
    if date_2:
        sudoku[5][5] = int(date_2 / 1000) % 10
        sudoku[6][6] = int(date_2 / 100) % 10
        sudoku[7][7] = int(date_2 / 10) % 10
        sudoku[8][8] = int(date_2 / 1) % 10
    return sudoku

def get_date(first):
    if first:
        msg = "Please, enter 1st date, and then press enter:"
    else:
        msg = "Please, enter 2nd date, and then press enter:"
    msg += "\n"
    msg += "Be careful, as a Sudoku do not use the number 0, if you have some in your date, they will be replaced by another number."
    msg += "\n"
    nb = None
    while nb == None:
        nb = input(msg)
        try:
            nb = int(nb)
            print("Your number is: ", nb)
            valid = input("If you are satisfied enter 'y':\n")
            if "y" != valid:
                nb = None
        except:
            print("Your date could not be converted to integer, try again")
            msg = "Please enter a date (for example '1914'):\n"
            nb = None
    return nb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="Date as inputs: INT INT", type=int, nargs=2)
    args = parser.parse_args()
    if args.date == None:
        d1 = get_date(True)
        d2 = get_date(False)
    else:
        d1 = args.date[0]
        d2 = args.date[1]
    s_base = sudoku=get_base(d1, d2)
    print("\033[2J")
    s = Sudoku(s_base)
    s = s.solve()
    if s == None:
        print("Your dates makes the sudoku unsolvable !")
    else:
        print(s)
