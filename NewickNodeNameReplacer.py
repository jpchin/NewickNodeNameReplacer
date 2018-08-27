#A script which requires a Newick formatted tree and the FASTA file which it was
#made from, and replaces the Newick node headers with the corresponding FASTA
#header from the FASTA input file.  Sequences in each file do not need to be in
#the same order, the script will match Accessions in the Newick file to Accessions
#in the FASTA file.

if __name__ == "__main__":
    #Stuff for file selection dialogue boxes:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()


    #Get a FASTA file to open
    gettingLocation = True
    #While a file hasn't been selected:
    while (gettingLocation == True):
        print("\nPlease choose an input file with FASTA sequences: ")
        inputFASTALocation = filedialog.askopenfilename()
        #Try opening the selected file, if successful set as FASTAData and continue
        try:
            inputFASTA = open(inputFASTALocation,"r")
            FASTAData = inputFASTA.read()
            gettingLocation = False
        #If the file can't be opened alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")


    #Get a Newick file to open
    gettingLocation = True
    #While a file hasn't been selected:
    while (gettingLocation == True):
        #Try opening the selected file, if successful set as NewickData and continue
        print("\nPlease choose an input file with a Newick format tree: ")
        inputNewickLocation = filedialog.askopenfilename()
        try:
            inputNewick = open(inputNewickLocation,"r")
            NewickData = inputNewick.read()
            gettingLocation = False
        #If the file can't be opened alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")
    
    #Get a file location to save the output data
    gettingLocation = True
    #Try opening the selected file, if successful set as outputFileLocation and continue
    while (gettingLocation == True):
        print("\nPlease choose an output file location and file name: ")
        outputFileLocation = filedialog.asksaveasfilename()
        try:
            file = open(outputFileLocation,"w")
            gettingLocation = False
        #If the file can't be opened alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")


           
    #Count the number of ">" chars to figure out how many sequences are in the file
    numberOfSeqs = FASTAData.count(">")
    print("There are " + str(numberOfSeqs) + " sequences in this file")
    
    #Create a list to read sequences into
    seqsList = []
    
    #Find sequences in the FASTA file and append them to the seqsList list.
    #Split sequences into accession numbers, the rest of the header, and the rest
    #of the sequence for manageability.
    
    #For every ">" char (which denotes the start of a sequence)
    for x in range (0, numberOfSeqs):

        #Find the end of the accession by finding the space character
        accessionEnd = FASTAData.find(" ")
        #Find the end of the header by finding the next return
        headerEnd = FASTAData.find("\n")
        #Find the *NEXT* ">" char (i.e. the start of the next sequence)
        secondSeqStart = FASTAData.find(">", 1)
        #Create a dictionary with the accession, header and sequence under separate items
        dictionary = {"accession":FASTAData[1:accessionEnd],\
                      "header":FASTAData[accessionEnd:headerEnd],\
                      "sequence":FASTAData[headerEnd:secondSeqStart]\
                      }
        #Append this dictionary to the seqsList list
        seqsList.append(dictionary)
        #Scrub the processed sequence from the input data
        FASTAData = FASTAData[secondSeqStart:]

    #Split the Newick tree into separate lines which are handled separately
    NewickData = NewickData.splitlines()
    
    with open(outputFileLocation, "a") as file:
        #For each line in the Newick tree:
        for line in NewickData:
            #If the line begins with a letter (i.e. is a node)
            if line[0].isalpha():
                #Find the accession number in the line
                endOfAccession = line.find(":")
                newickAccession = line[:endOfAccession]
                #Remember where the rest of the line begins
                restOfLine = line[endOfAccession:]

                #For each sequence in the input file:
                for seq in seqsList:
                    #If the Newick line's accession is the same as the sequence's accession
                    if (newickAccession == seq["accession"]):
                        #The new line for the Newick tree is the accession + sequence header
                        newLine = seq["accession"] +  seq["header"] + restOfLine
                        #Scrub all spaces and square brackets, because some tools dislike them
                        newLine = newLine.replace(" ", "-")
                        newLine = newLine.replace("[", "")
                        newLine = newLine.replace("]", "")
                        #Write the new line to the file
                        file.write(newLine)
            #Otherwise the line needs no modification, so write it to the output file directly.
            else:
                file.write(line)

    print("Done!")



