def writeFile(string, filename):

    print('\n-writeFile-\n')
    
    finalFILE = open(filename + ".txt", 'a+')
    finalFILE.write(string)

    finalFILE.close()
