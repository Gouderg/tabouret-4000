import os
import shutil

class FileWriter:
    
    def __init__(self, path):
        self.path = path
        self.verrou = ".verrou"
    
    def clean(self):
        if os.path.isfile(self.path):
            os.remove(self.path)
        if os.path.isfile(self.verrou):
            os.remove(self.verrou)

    def readFile(self):
        fileContent = []

        # Verify if file not exist
        if not os.path.isfile(self.path):
            print("Fichier n'existe pas, impossible de lire les donnnés")
            return fileContent

        # Verify if not one is using the file.
        if os.path.isfile(self.verrou):
            print("Le fichier verrou est présent, quelqu'un utilise les donnnées.")
            return fileContent

        # Create the lock.file
        with open(self.verrou, "w") as file:
            file.write("he")

        # Read the data from the file.
        with open(self.path, "r") as file:
            for row in file:
                row = [float(a) for a in row.replace("\n", '').split(' ')]
                fileContent.append(row)

        # Remove the lock file.
        if os.path.isfile(self.verrou):
            os.remove(self.verrou)

        return fileContent
    
    def writeFile(self, lineToWrite):
        # Read the data from the file.
        fileContent = self.readFile()

        # Verify if not one is using the file.
        if os.path.isfile(self.verrou):
            print("Le fichier verrou est présent, quelqu'un utilise les donnnées")
            return -1

        # Create the lock.file
        with open(self.verrou, "w") as file:
            file.write("he")

        if len(fileContent) > 5:
            fileContent.pop(0)
        fileContent.append(lineToWrite)

        
        with open(self.path, "w") as file:
            print("writing")
            for row in fileContent:
                txtToWrite = ' '.join([str(b) for b in row]) + "\n"
                file.write(txtToWrite)
        
        # Remove the lock file.
        if os.path.isfile(self.verrou):
            os.remove(self.verrou)
        
        return 1

# if __name__ == "__main__":
#     f = FileWriter("data.txt")

#     f.writeFile([1, 4, 9090909, 3, -4])
#     f.writeFile([1, 4, 9090909, 3, -4])
#     print(f.readFile())