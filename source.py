# 3D Laser Scanner conversion script.

# Import relevent modules.
import Image,sys,os

# Format filename string to suit the camera output.
# Assumes sequential numbering.
fss = "DSC_0"
sNum = 244 #244
fes = ".JPG"
os.chdir ("Images")
fNum = sNum
fName = fss+str(fNum)+fes

# Count how many files we have to process.
fCount = 0
while True:
    fName = fss+str(fNum)+fes
    try:
        inFile = Image.open(fName)
    except IOError:
        break
    fNum += 1
    fCount += 1
fNum = sNum
fName = fss+str(fNum)+fes
print fCount, "Files to process..."
if fCount == 0: sys.exit(0)

# Set up some variables for the processing loop.
sla = slt = slb = 0.0
th = 50
step = 10
xSize,ySize = 250,250
oyPos = 0

# Create output file in RGB mode.
outFile = Image.new("RGB",(xSize,fCount),0)
outPix = outFile.load()

loop = True
while loop:
    try:
        print"Attempting load",fName
        inFile = Image.open(fName)
    except IOError:
        print"Load failed."
        print"End of files."
        break

    print "Resizing",inFile.size,"to",xSize,ySize
    sPic = inFile.resize((xSize,xSize),Image.ANTIALIAS)
    inPic = sPic.load()
    print"Scanning",fName,
    
    # Processing routine here.....
    for x in range(0,xSize):
        bp = slt = slb = -1
        for y in range(0,ySize,1):
            r,g,b = inPic[x,y]
            if r > th > bp:
                bp = r
                slt = y
        bp = -1
        for y in range(ySize-1,0,-1):
            r,g,b = inPic[x,y]
            if r > th > bp:
                bp = r
                slb = y
        sla = (slt+slb)/2
        sla = (sla-70)*6
        if sla < 0:sla = 0
        if sla > 255: sla = 255
        outPix[x,oyPos] = sla,sla,sla

    print" ...complete."
    print""
    fCount -= 1
    print fCount,"Files to process..."
    oyPos += 1
    fNum += 1
    fName = fss+str(fNum)+fes
    fSaveX = "lr"+str(fNum)+fes
    sPic.save(fSaveX)
# Save output file
outFile.save("zmap.jpg")
