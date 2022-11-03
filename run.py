from pathlib import Path


#data = Path('Qx1Csp.rnd').read_bytes()
#print(data[:5])

filename = '1st_file.bin'
filenames = ['1st_file.bin', '2nd_file.bin', '3rd_file.bin']
numberOfFiles = len(filenames)


def readBytes(filename, nBytes):

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


allfiles = []

for x in range(numberOfFiles):
    filecontent = []
    
    for b in readBytes(filenames[x], 32):
        i = int.from_bytes(b, byteorder='big')
        filecontent.append(bin(i))
        #print(f"raw({b}) - int({i}) - binary({bin(i)})")
    
    allfiles.append(filecontent)
  

    
print("Number of files: " + str(len(allfiles)))
listPrimary = allfiles[0]
print(listPrimary)
#print(len(allfiles[0]))
#Longest common string between one file and others:

#print(allfiles[0][0] == allfiles[1][0])

others = len(allfiles)-1
otherFiles = allfiles[-others:]

#token = allfiles[0][0]

#test = [1,2,3,4,5,6]
#test2 = [7,8,3,4,55,66]
#print(test[2:4] == test2[2:5])
#out = test[2:4]
#print(out)

    
#token = []
#token.append(allfiles[0][0])
print(otherFiles)
#print("Token = " + str(token))

    
    
for tokenPosStart in range(0, len(allfiles[0])):
        
    token = []

    maxTokenLength = 0    
    for tokenPos in range(tokenPosStart, len(allfiles[0])):
   
        token.append(allfiles[0][tokenPos]) #produce token
                 
        for filenumber in range(len(otherFiles)):   #compare to other files            
            pos = 0
            
            while pos < (len(otherFiles[filenumber])-1):
            
                test = otherFiles[filenumber][pos:pos+len(token)]

                if (token == test) & (len(token) >= 4): #length filter to be omitted
                    #save found substring                  
                    print("Found: " + str(token))

                    for x in token:
                         print(chr(int(x,2)), end='')
                    print('')
                pos += 1