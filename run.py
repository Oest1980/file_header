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


def compare_files(filenames: list[Path]) -> dict[int, str]:
    
    numberOfFiles = len(filenames)
    allfiles = []

    for x in range(numberOfFiles):
        filecontent = []
        
        for b in readBytes(filenames[x], 320):
            i = int.from_bytes(b, byteorder='big')
            filecontent.append(bin(i))
            #print(f"raw({b}) - int({i}) - binary({bin(i)})")
        
        allfiles.append(filecontent)
    

        
    print("Number of files: " + str(len(allfiles)))

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


def main(args=None):
    #print(sys.argv[1:])
    folder = sys.argv[1:][0]
    print(folder)

    files = os.listdir(folder)

    paths: list[Path] = []    

    for file in files:
        #print(file)

        path_file = Path(folder + "\\" + file)
        print(path_file)

        if path_file.exists():
            paths.append(path_file)
            

    for i in range(len(paths)): #rotate primary file through list
        print(paths)
        print(compare_files(paths))
        paths = rotatePaths(paths)


#run with:
#python .\run.py C:\temp\testfolder




if __name__ == "__main__":
    main()