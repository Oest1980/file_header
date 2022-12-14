from pathlib import Path
import sys, os

#data = Path('Qx1Csp.rnd').read_bytes()
#print(data[:5])

filename = '1st_file.bin'
filenames = ['1st_file.bin', '2nd_file.bin', '3rd_file.bin']


def readBytes(filename, nBytes):

    try:
        with open(filename, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte:
                    yield byte
                else:
                    break
                
                if nBytes > 0:
                    nBytes -= 1
                    if nBytes == 0:
                        break
    except EnvironmentError:
        print("Access error: Can't open file...")


def compare_files(filenames: list[Path], header_size: int = None) -> dict[int, str]:
    
    #print("header_size = " + str(header_size))

    numberOfFiles = len(filenames)
    allfiles = []

    for x in range(numberOfFiles):
        filecontent = []
        
        for b in readBytes(filenames[x], header_size):
            i = int.from_bytes(b, byteorder='big')
            filecontent.append(bin(i))
            #print(f"raw({b}) - int({i}) - binary({bin(i)})")
        
        allfiles.append(filecontent)
    

        
    #print("Number of files: " + str(len(allfiles)))

    listPrimary = allfiles[0]
    #print(listPrimary)
    others = len(allfiles)-1
    otherFiles = allfiles[-others:]
    #print(otherFiles)
    
    results: dict[int, str] = {}
        
    maxTokenLength = 0
    for tokenPosStart in range(0, len(allfiles[0])):
            
        token = []
            
        for tokenPos in range(tokenPosStart, len(allfiles[0])):
    
            token.append(allfiles[0][tokenPos]) #produce token
                    
            for filenumber in range(len(otherFiles)):   #compare to other files            
                pos = 0
                
                while pos < (len(otherFiles[filenumber])-1):
                
                    test = otherFiles[filenumber][pos:pos+len(token)]

                    if (token == test) & (len(token) >= 4): #length filter to be omitted
                        #save found substring                  
                        #print("Found: " + str(token))

                        found: str = ""
                        for x in token:
                            #concat = chr(int(x,2))
                            concat = hex(int(x,2)).replace('0x', '')
                            if len(concat) == 1:
                                concat = "0" + concat

                            found = found + concat

                        #print("filenumber = " + str(filenumber))
                        #print(found)

                        if len(found) >= maxTokenLength:    #maximize length of common token
                            maxTokenLength = len(found)
                            results[filenumber + 1] = found

                    pos += 1

    return results    

def rotatePaths(paths: list[Path]) -> list[Path]:
    rotate = paths.pop(0)
    paths.append(rotate)
    
    return paths


histogram: dict[str, int] = {}

def main(args=None):
    #print(sys.argv[1:])
    
    if sys.argv[1] == "--help":
        print("Arguments are: folder & header size")
        sys.exit(0)
    elif sys.argv[1] == "--version":
        print("Version 0.1.0")
        sys.exit(0)
    #elif len(sys.argv) < 3:
    #    print("Error less than two arguments, two needed.")
    #    sys.exit(0)

    folder = sys.argv[1]
    if len(sys.argv) == 3:
        header_size = int(sys.argv[2])
    else:
        header_size = 320
        print("Header size = " + str(header_size))
    #print(header_size)
    print(folder)


    # files = os.listdir(folder)

    paths: list[Path] = [f for f in Path(folder).iterdir() if f.is_file()]    

    # for file in files:
    #     #print(file)

    #     path_file = Path(folder, file)
    #     print(path_file)

    #     if path_file.exists():
    #         paths.append(path_file)
            
    print("Number of files: " + str(len(paths)) + "\n")

    for i in range(len(paths)): #rotate primary file through list
        #print(paths)               
        results_dict = compare_files(paths, header_size)
        #print(results_dict)

        print("The longest common string between file({path}) and the following files are:".format(path=paths[0]))
        for key, value in results_dict.items():
            print(str(paths[key]) + " - strengen er: " +str(value))

        print("\n")

        paths = rotatePaths(paths)


#run with:
#python .\run.py C:\temp\testfolder




if __name__ == "__main__":
    main()