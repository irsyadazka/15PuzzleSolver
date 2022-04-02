from heapq import heappush, heappop
import time, random

compareMatrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]] # matrix yang akan di compare
row16 = 0  # row elemen kosong
col16 = 0 # column elemen kosong
solveable = False
countNodes = 0
listValidMoves = [] # list yang berisi arah yang valid
stop = 0
getSolution = False

# class PriorityQueue
class PrioQueue:
    # Constructor
    def __init__(self):
        self.heap = []

    # Method push based on value
    def push(self, value):
        heappush(self.heap, value)

    # Method pop minimum element
    def pop(self):
        return heappop(self.heap)

    # Method isEmpty
    def isEmpty(self):
        if not self.heap:
            return True
        return False

# class Node
class Node:
    # Constructor
    def __init__(self, root, matrix, emptyPosRow, emptyPosCol, diff, depth, move):
        self.root = root
        self.matrix = matrix
        self.emptyPosRow = emptyPosRow
        self.emptyPosCol = emptyPosCol
        self.diff = diff
        self.depth = depth
        self.move = move

    # Method agar prioQueue terbentuk berdasarkan nilai diff
    def __lt__(self, other):
        return self.diff < other.diff

# fungsi mencari indeks elemen
def findLocElmt(num, inMatrix):
    for row in range(4):
        for col in range(4):
            if inMatrix[row][col] == num:
                return row, col

# fungsi mencari jumlah dari kurangI
def kurangI(num, inMatrix):
    row, col = findLocElmt(num, inMatrix)
    count = 0
    if col != 3:
        for i in range(col, 3):
            if inMatrix[row][i+1] < num:
                count += 1
    if row != 3:
        for i in range(row + 1, 4):
            for j in range(4):
                if inMatrix[i][j] < num:
                    count += 1
    return count

# fungsi untuk mengecek apakah matriks dapat diselesaikan
def isSolveable(inMatrix):
    global row16, col16, solveable
    row16, col16 = findLocElmt(16, inMatrix)
    if (row16 + col16) % 2 == 1:
        sigma = 1 # nilai X posisi yang diarsir
    else:
        sigma = 0 # nilai X posisi yang tidak diarsir
    for i in range(4):
        for j in range(4):
            # print nilai kurangI dari elemen
            print(compareMatrix[i][j], "\t:\t", kurangI(compareMatrix[i][j], inMatrix), end="\n")
            # tambahkan ke dalam nilai sigma
            sigma += kurangI(inMatrix[i][j], inMatrix)
    print("\nNilai dari Sigma Kurang(i)\t=\t", sigma, end="\n")
    if sigma % 2 == 0:
        solveable = True

# fungsi mencari jumlah elemen yang berbeda terhadap compareMatrix
def getDiff(inMatrix):
    global countNodes

    diff = 0
    for i in range(4):
        for j in range(4):
            if inMatrix[i][j] != compareMatrix[i][j] and inMatrix[i][j] != 16:
                diff += 1
    countNodes += 1 # menambah jumlah node yang dibangkitkan
    return diff

# fungsi mencari daftar move yang valid berdasarkan posisi dan recent moves
def validMove(row, col, move):
    global listValidMoves
    listValidMoves = []
    if row != 0 and move != "Move Down":
        listValidMoves.append("Move Up")
    if row != 3 and move != "Move Up":
        listValidMoves.append("Move Down")
    if col != 0 and move != "Move Right":
        listValidMoves.append("Move Left")
    if col != 3 and move != "Move Left":
        listValidMoves.append("Move Right")

# fungsi bergerak ke atas
def moveUp(row, col):
    return row - 1, col

# fungsi bergerak ke bawah
def moveDown(row, col):
    return row + 1, col

# fungsi bergerak ke kiri
def moveLeft(row, col):
    return row, col - 1

# fungsi bergerak ke kanan
def moveRight(row, col):
    return row, col + 1

# fungsi copy matrix
def cloneList(li):
    newList = [[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            newList[i][j] = li[i][j]
    return newList

# fungsi membuat child node
def makeNode(matrix, emptyPosRow, emptyPosCol, newPosRow, newPosCol, depth, parent, move):
    cloneMatrix = cloneList(matrix)

    # swap elemen
    cloneMatrix[emptyPosRow][emptyPosCol], cloneMatrix[newPosRow][newPosCol] = cloneMatrix[newPosRow][newPosCol], cloneMatrix[emptyPosRow][emptyPosCol]

    diff = getDiff(cloneMatrix) 
    diff += depth # tambahkan nilai depth

    childNode = Node(parent, cloneMatrix, newPosRow, newPosCol, diff, depth, move)
    return childNode

# fungsi print puzzle
def printMatrix(result):
    for row in range(4):
        for col in range(4):
            if result[row][col] == 16:
                if col == 3:
                    print("-", end="\n")
                else:
                    print("-", end="\t")
            else:
                if col == 3:
                    print(result[row][col], end="\n")
                else:
                    print(result[row][col], end="\t")
    print()

# fungsi print rute dari root ke ditemukannya solusi
def printRoutes(root):
    if root == None:
        return
    
    printRoutes(root.root)
    print("Step taken: " + root.move)
    printMatrix(root.matrix)
    print()

# fungsi untuk mencari solusi
def findSolution(inMatrix):
    global listValidMoves, countNodes, stop, getSolution
    # membuat PrioQueue
    liveNode = PrioQueue()

    diff = getDiff(inMatrix)

    # membuat root node
    root = Node(None, inMatrix, row16, col16, diff, 0, "Root")

    # menambahkan root node ke dalam PrioQueue
    liveNode.push(root)

    # looping untuk mencari solusi
    while not liveNode.isEmpty() and time.time() - start < 180:
        getNode = liveNode.pop()
        if getNode.diff == 0 or getNode.diff == getNode.depth:
            stop = time.time()
            getSolution = True
            printRoutes(getNode) # print rute dari root ke ditemukannya solusi
            countNodes -= 1 # kurangi jumlah node yang dibangkitkan karena dihitung root
            return

        # check daftar valid move pada node ini
        validMove(getNode.emptyPosRow, getNode.emptyPosCol, getNode.move)
        for move in listValidMoves:
            if move == "Move Up":
                newPosRow, newPosCol = moveUp(getNode.emptyPosRow, getNode.emptyPosCol)
            if move == "Move Down":
                newPosRow, newPosCol = moveDown(getNode.emptyPosRow, getNode.emptyPosCol)
            if move == "Move Left":
                newPosRow, newPosCol = moveLeft(getNode.emptyPosRow, getNode.emptyPosCol)
            if move == "Move Right":
                newPosRow, newPosCol = moveRight(getNode.emptyPosRow, getNode.emptyPosCol)
            
            # membuat child node
            childNode = makeNode(getNode.matrix, getNode.emptyPosRow, getNode.emptyPosCol, newPosRow, newPosCol, getNode.depth + 1, getNode, move)
            # tambahkan child node ke dalam PrioQueue
            liveNode.push(childNode)

# fungsi membangkitkan puzzle random
def createMatrixRandom():
    listElement = list(range(1, 17))
    random.shuffle(listElement)
    matrix = [[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            matrix[i][j] = listElement[i*4 + j]
    return matrix

# Main
# program akan menghandle jika terjadi error pada masukan file
try:
    print("\n15 Puzzle Solver with Branch and Bound Algorithm\n")
    print("\nDaftar Pilihan Mode :\n1. Random\n2. Input File")
    mode = int(input("\nPilih mode : "))
    if mode == 1:
        print("\nPerhatikan bahwa mode ini dapat membuat looping program sangat banyak\nhingga tidak dapat dilanjutkan!")
        print("\nApakah anda yakin ingin melanjutkan? (y/n)\n")
        if input("(y/n) : ") == "y":
            l = createMatrixRandom()
        else:
            print("\nProgram dihentikan\n")
            exit()
    if mode == 2:
        filename = input("\nMasukkan nama file puzzle yang ingin dicari solusinya: ")
        file = "../test/" + filename + ".txt"
        # proses pembentukan matriks dari file
        with open(file, 'r') as f:
            l = [[int(num) for num in line.split(' ')] for line in f]
    print("Puzzle yang akan dicari adalah seperti berikut:\n")
    printMatrix(l)
    print("Nilai Kurang(i) untuk setiap ubin adalah sebagai berikut:\n")
    isSolveable(l)
    if not solveable:
        print("\nPersoalan ini tidak dapat menghasilkan solusi\n")
    else:
        print("\nPersoalan ini dapat diselesaikan dengan langkah sebagai berikut:\n")
        start = time.time()
        findSolution(l)
        if getSolution:
            print("Finished!\n\nSimpul dibangkitkan\t=\t", countNodes)
            print("Time execution\t\t=\t", stop - start, "sekon\n")
        else: # program akan berhenti jika tidak waktu sudah mencapai limit
            print("\nPersoalan terlalu lama dieksekusi, tidak dapat dilanjutkan\n\nExiting...\n")
except:
    # keluaran jika terjadi error dalam input nama file
    print("\nFile masukan tidak tersedia, silahkan run program & coba lagi")
    print("\nExiting...\n")