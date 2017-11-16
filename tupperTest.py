import sys
from os import listdir, getcwd

def loadFiles(argv):

    print("\n-loadFiles-\n")

    files = []

    if len(argv) > 1:
        
        # In case of using terminal to load te files

        for i in range(1,len(argv)-1):

            filename = argv[i]
            if ".txt" in filename:
                files.append(open(filename, 'r'))
            

    else:

        # In case of using the automatic moe to load the files
            
        for filename in listdir("input_files"):
            if ".txt" in filename:
                files.append(open(filename, 'r'))
            else:

                print(filename+" is not a txt file")


    return files

def main(argv):

    print(len(argv))

    files = loadFiles(argv)

    # for f in files:
    #     s = f.read()
    #     print(s)


if __name__ == "__main__":
    main(sys.argv)
