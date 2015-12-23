__author__ = 'huziy'


import numpy as np
import matplotlib.pyplot as plt

def plot(path = "Titre0.csv"):
    f = open(path)
    lines = f.readlines()
    lines = lines[1:]
    mediansData = []
    for theLine in lines:
        theLine = theLine.strip()
        if theLine == "": continue
        fields = theLine.split(",")
        fields = fields[1:-1]
        fields = map(float, fields)
        mediansData.append(np.median(fields))

    #plt.plot(mediansData, label = path)
    mediansData = np.array(mediansData)
    mediansData = np.reshape(mediansData, (5, -1))

    meanEvolution = np.mean(mediansData, axis=0)

    plt.plot(meanEvolution, label=path)

    print "\"" + path + "\"" + ": ", meanEvolution[-1] - meanEvolution[0] , ","


if __name__ == "__main__":

    for i in xrange(10):
        plot(path = "Titre%d.csv" % i)

    #plot(path="Index.csv")
    plt.legend()
    plt.show()