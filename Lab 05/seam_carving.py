# Selinie Wang (jw6qe)
# Algorithms HW5

# Collaborators: Jenny Yao, countless hours in OH

import math

class SeamCarving:
    def __init__(self):
        self.image = []
        self.values = []
        self.esum = []
        self.seam = []
        return

    # distance method to find distance between two pixels
    def distance(self, x1, y1, x2, y2):
        dist = (self.image[x2][y2][0] - self.image[x1][y1][0]) ** 2 + \
               (self.image[x2][y2][1] - self.image[x1][y1][1]) ** 2 + \
               (self.image[x2][y2][2] - self.image[x1][y1][2]) ** 2
        sqrtdist = math.sqrt(dist)
        return sqrtdist

    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    #
    # @return the seam's weight
    def run(self, image):
        self.image = image
        self.values = 0
        self.esum = 0

        # create a 2d matrix to store seams
        w, h = len(image), len(image[0])
        self.values = [[0 for j in range(h)] for i in range(w)]
        # print("Values: ", self.values)

        # Four corner cases (top left, top right, bottom left, bottom right)
        energytl = (self.distance(0,0,1,0) + self.distance(0,0,0,1)) / 2
        self.values[0][0] = energytl

        energytr = (self.distance(len(image)-1,0,len(image)-2,0) +
                    self.distance(len(image)-1,0,len(image)-1,1)) / 2
        self.values[len(image)-1][0] = energytr

        energybl = (self.distance(0,len(image[0])-1,1,len(image[0])-1) +
                    self.distance(0,len(image[0])-1,0,len(image[0])-2)) / 2
        self.values[0][len(image[0])-1] = energybl

        energybr = (self.distance(len(image)-1,len(image[0])-1,len(image)-2,len(image[0])-1) +
                    self.distance(len(image)-1,len(image[0])-1,len(image)-1,len(image[0])-2)) / 2
        self.values[len(image)-1][len(image[0])-1] = energybr
        # print("Value:", self.values)


        # Four edge cases (horizontal top, horizontal bottom, vertical left, vertical right)
        for c in range(1, len(image) - 1):
            energyht = ((self.distance(c,0,c+1,0) + self.distance(c,0,c,1) +
                        self.distance(c,0,c-1,0)) / 3)
            self.values[c][0] = energyht

        for c in range(1, len(image) - 1):
            energyhb = ((self.distance(c,len(image[0])-1,c,len(image[0])-2) +
                        self.distance(c,len(image[0])-1,c-1,len(image[0])-1) +
                        self.distance(c,len(image[0])-1,c+1,len(image[0])-1)) / 3)
            self.values[c][len(image[0])-1] = energyhb

        for r in range(1, len(image[0]) - 1):
            energyvl = ((self.distance(0,r,1,r) +
                        self.distance(0,r,0,r+1) +
                        self.distance(0,r,0,r-1)) / 3)
            self.values[0][r] = energyvl

        for r in range(1, len(image[0]) - 1):
            energyvr = ((self.distance(len(image)-1,r,len(image)-1,r+1) +
                        self.distance(len(image)-1,r,len(image)-1,r-1) +
                        self.distance(len(image)-1,r,len(image)-2,r)) / 3)
            self.values[len(image)-1][r] = energyvr


        # Rest of the pixels other than corner/edge
        for c in range(1, len(image)-1):
            for r in range(1, len(image[0])-1):
                energy = ((self.distance(c,r,c+1,r) + self.distance(c,r,c,r+1) +
                          self.distance(c,r,c-1,r) + self.distance(c,r,c,r-1)) / 4)
                self.values[c][r] = energy

        # print("Pixel weight: ", self.values)

        # create another 2d matrix to store sum of energy
        w, h = len(self.values), len(self.values[0])
        self.esum = [[0 for row in range(h)] for col in range(w)]
        # self.esum = self.values
        for i in range(0, len(self.values)):
            self.esum[i][len(self.values[0])-1] = self.values[i][len(self.values[0])-1]

        # Find minimum energy
        for row in range(len(image[0])-2,-1,-1):
            for col in range(len(image)-1,-1,-1):
                # brute force to get minimum
                # left column (2 minimums)
                if col == 0:
                    self.esum[col][row] = min(self.esum[col][row+1], self.esum[col+1][row+1]) + self.values[col][row]
                # right column (2 minimums)
                elif col == len(image)-1:
                    self.esum[col][row] = min(self.esum[col][row+1], self.esum[col-1][row+1]) + self.values[col][row]
                # rest of the columns (3 minimums)
                else:
                    self.esum[col][row] = min(self.esum[col][row+1], self.esum[col-1][row+1],
                                              self.esum[col+1][row+1]) + self.values[col][row]

        # print("Energy sum: ", self.esum)

        # get the minimum value of first row
        minvalcolumn = min(self.esum)
        minval = minvalcolumn[0]
        weight = minval

        seamstart = self.esum.index(minvalcolumn)
        # for row in range(0, len(image[0])):
        #     for col in range(0, len(image)):

        self.seam = 0
        self.seam = [0 for j in range(0, len(self.image[0]))]
        # self.seam.append(seamstart)

        # print(seamstart)
        for row in range(0, len(image[0])):  # goes through each row
            # print("X:" , seamstart, "Y:", row)
            if row != len(image[0])-1:
                if seamstart == 0:
                    if min(self.esum[seamstart][row+1], self.esum[seamstart+1][row+1]) \
                            == self.esum[seamstart][row+1]:
                        self.seam[row] = seamstart
                    else:
                        self.seam[row] = seamstart + 1
                        seamstart = seamstart + 1
                elif seamstart == len(image)-1:
                    if min(self.esum[seamstart][row+1], self.esum[seamstart-1][row+1]) \
                            == self.esum[seamstart][row+1]:
                        self.seam[row] = seamstart
                    else:
                        self.seam[row] = seamstart - 1
                        seamstart = seamstart - 1
                else:
                    if min(self.esum[seamstart][row+1], self.esum[seamstart-1][row+1],
                        self.esum[seamstart+1][row+1]) == self.esum[seamstart][row+1]:
                        self.seam[row] = seamstart
                    elif min(self.esum[seamstart][row+1], self.esum[seamstart-1][row+1],
                        self.esum[seamstart+1][row+1]) == self.esum[seamstart-1][row+1]:
                        self.seam[row] = seamstart - 1
                        seamstart = seamstart - 1
                    else:
                        self.seam[row] = seamstart + 1
                        seamstart = seamstart + 1
            else:
                self.seam[row] = seamstart

        return weight

    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    #
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    #
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    #         as an array
    def getSeam(self):
        # seam = []
        return self.seam