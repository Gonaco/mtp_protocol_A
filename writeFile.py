def writeFile(string, filename):

    finalFILE = open(filename + ".txt", 'a+')
    finalFILE.write(string)

    finalFILE.close()
