import sys
import os.path
import cv2 as cv

# Function produces 3 images:
# _left : left camera image
# _right : right camera image
# _merged : merged (R and GB channels)
def process_file(path):
    print("--- Processing", path)

    # Check if file has extension
    if path.rfind(".") == -1:
        print("File has no extension")  
        return
    
    # Check if file exists
    if not os.path.isfile(path):
        print("File does not exist")
        return       

    filename = os.path.split(path[:path.rfind(".")])[1]

    # Get file data
    fh = open(path, "rb")
    data = fh.read()
    fh.close()

    # Find index of split
    index = data.find(b'\xff\xd9\xff\xd8\xff')
    offset = 0

    # Check if split exists
    if (index == -1):
        # Try with a gap
        index = data.find(b'\xff\xd9\x00\xff\xd8\xff')
        if (index == -1):
            print("File split not found. May not be a 3D image")
            return
        offset = 1

    leftfile = filename + "_left.jpg"
    rightfile = filename + "_right.jpg"

    # First image
    fh = open(leftfile, "wb")
    fh.write(data[:index+2])
    fh.close()

    # Second image
    fh = open(rightfile, "wb")
    fh.write(data[index+2+offset:])
    fh.close()

    image_left = cv.imread(leftfile)

    #BGR
    image_left[:,:,0] = 0
    image_left[:,:,1] = 0

    image_right = cv.imread(rightfile)
    #BGR
    image_right[:,:,2] = 0

    image_combined = cv.merge((image_right[:,:,0], image_right[:,:,1], image_left[:,:,2]))

    # Save combined
    mergedfile = filename+"_merged.jpg"
    cv.imwrite(mergedfile, image_combined)

    #print("Split! Output as", leftfile + ",", rightfile + ",", "and", mergedfile)


to_process = []
files = os.listdir()

# Get list of MPO files in current folder
for file in files:
    if file.lower().endswith(".mpo"):
        to_process.append(file)

# Make processed folder if not exist
if not os.path.isdir("processed"):
    os.makedirs("processed")

os.chdir("processed")

print("Processing", len(to_process), "files...")

print(to_process)

for file in to_process:
    process_file(os.path.join("../",file))