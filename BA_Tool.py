"""
TUI Tool for ImageJ/Fiji - by André Wolf
Version: 0.005
"""
# importing used packages
import os
import tkinter as tk
from tkinter import filedialog
import imagej
import time


"""
Requirements:
Java JDK
Apache Maven (save in environment variables (PATH))

"""

global directories # List for all the directories
directories = []
global ij # ImageJ instance 


def get_directory(path_index): # Fills the directories with the current directories available and returns the selected one
    try:
        if os.path.exists("file_paths.txt"):
            directories = []
            with open("file_paths.txt", "r") as file:
                for line in file:
                    directories.append(line.strip()) # cleanses the directory of unwanted " " and "\n" and saves them one by one in list (directory)
            return directories[path_index]
    except IndexError:
        print("\n |||||| Error occured! Index out of bounds |||||| \n")
    except Exception as e:
        print(f"\n |||||| Error occurred! {e} \n")
    finally:
        print("Returning to the selection menu... \n")
        selection()

def get_directory_by_name(name):
    try:
        if os.path.exists("file_paths.txt"):
            with open("file_paths.txt", "r") as file:
                for line in file:
                    if name in line.strip():
                        return line.strip()
    except Exception as e:
        print(f"\n |||||| Error occurred! {e} \n")
    finally:
        print("Returning to the selection menu... \n")
        selection()


def initialize():
    global ij
    os.system("cls")
        # Pfad zur Fiji App und zu den Plugins
    print("Searching for directories...\n")
    if os.path.exists("file_paths.txt"):
        fiji_path = get_directory(0)
        plugin_path = get_directory(1)
    else:
        print("Please select Fiji.app root folder:")
        TKroot = tk.Tk()
        TKroot.withdraw()
        fiji_path = filedialog.askdirectory(title="Choose Fiji.app folder:")
        with open("file_paths.txt", "a") as file:
            file.write(fiji_path + "\n")
        print("Please select Fiji.app/plugins folder:\n\n")
        plugin_path = filedialog.askdirectory(title="Choose Fiji.app/plugins folder:")
        with open("file_paths.txt", "a") as file:
            file.write(plugin_path + "\n")

    # Configurs the ImageJ/Fiji instance (here: mode="interactive" = with interactive GUI)
    print("Starting ImageJ/Fiji...")
    ij = imagej.init(fiji_path, mode='interactive')
    print(f"ImageJ version: {ij.getVersion()}")

    # Füge das Plugin-Verzeichnis zum Classpath hinzu
    classpath = os.path.join(plugin_path, "*")
    os.environ["CLASSPATH"] = classpath + ";" + os.environ.get("CLASSPATH", "")

    # Starte die Fiji-Anwendung
    ij.ui().showUI()




def folder_hierarchie():
    os.system("cls")
    print("Creating a result folder hierarchie...")
    # Root folder for all future results
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')  # Pfad zum Desktop
    root_path = os.path.join(desktop_path, "Results") 
    #root_path = os.path.join(os.getcwd(), "TEMP_FOLDER") #creates root folder to fiji.app root folder for some reason?
    # List of subfolder to create (extendable for later)
    subfolder = ["Classifier", "ResultsLeafMeasurements", "SegmentedLeaves", "StitchingFolder"]

    if not os.path.exists(root_path):
        os.makedirs(root_path)
        # Writes directory in file for future use
        with open("file_paths.txt", "a") as file:
            file.write(root_path + "\n")

    # Creating subfolder to root folder for later savings of measurements and segmentations etc. 
    for sub_name in subfolder:
        sub_path = os.path.join(root_path, sub_name)
        # Writes directory in file for future use
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
            with open("file_paths.txt", "a") as file:
                file.write(sub_path + "\n")
    selection()


def open_folder():
    os.system("cls")
    if os.path.exists("file_paths.txt"):
        with open("file_paths.txt", "r") as file:
            for i, line in enumerate(file,0):
                print(f"[{i}]: {line.strip()}" + "\n")  # cleanses the directory of unwanted " " and "\n" and saves them one by one in list (directory)
        print("==============================" + "\n")
        sure = input("Please select one of the above directoories by number to open:")
        sure = int(sure)
        if sure > i:
            print("Invalid input, choose again...\n")
            time.sleep(2)
            os.system("cls")
            open_folder()
        else:
            os.startfile(get_directory(sure))
            print("Selected directory is now open...")
    else:
        print("file_paths.txt not found!")
    selection()


def stitching(): ###################################################################################################################################################################################################
    os.system("csl")
    print("Please save all the related pictures in one folder, each specimen individually!")

    """
    1. Directory of one sample with multiple pictures
    2. Multiple samples available
        opt1: asking to save them individually and re-do the process
        opt2: itterate through... what?
    """
    stitching_folder = get_directory("StitchingFolder")
    try:
        ij.py.run_plugin("Stitch Directory with Images (unknown configuration)", "image_directory=[{stitching_folder}] output_file_name=TileConfiguration.txt rgb_order=rgb channels_for_registration=[Red, Green and Blue] fusion_method=[Linear Blending] fusion_alpha=1.50 regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50")
    except:
        print("|||||| Error occured. Going back... ||||||")
    selection()


def selection():    # Creates a "GUI" to select one of the given options
    #while True:
        print("\n[1] Folder Hierarchie \n\n[2] Open Folder \n\n[3] Stitching multiple images \n\n[4] PLACEHOLDER \n\n[5] PLACEHOLDER \n\n[6] PLACEHOLDER \n\n[7] PLACEHOLDER \n\n[0] Exit Program")
        print("TESTS: [-] | [+]") #DELETE AT THE END
        sel = input("\n\n Choose an option by number to proceed: ")

        if sel == "1":
            folder_hierarchie()
        elif sel == "2":
            open_folder()
        elif sel == "3":
            stitching()
        elif sel == "4":
            pass
        elif sel == "5":
            pass
        elif sel == "6":
            pass
        elif sel == "7":
            pass
        elif sel == "8":
            pass
        elif sel == "9":
            pass
        
        #TESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTEST
        elif sel == "-":
            #ij.py.run_plugin("Pairwise stitching", "")
            try:
                ij.py.run_plugin("Stitch Directory with Images (unknown configuration)", "image_directory=[M:/Benutzer/Studium/Biologie/Bachelorarbeit/Programme & Scripts/Pipeline/xx_StitchingTempFolder] output_file_name=TileConfiguration.txt rgb_order=rgb channels_for_registration=[Red, Green and Blue] fusion_method=[Linear Blending] fusion_alpha=1.50 regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50")
            except:
                print("|||||| Error occured. Going back... ||||||")
            selection()

        elif sel == "+":
            path = get_directory_by_name(True)
            print(path)
            pass	
        #TESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTESTTESTESTESTESTESTESTESTESTESTESTESTESTEST

        elif sel == "0":
            sure = input("Are you sure? (Y/1) | (N/0): ")
            sure = sure.lower()
            if  sure == 'y' or sure == "yes" or sure == "1":
                os.system("cls")
                print("Stopping program...")
                time.sleep(2)
                os.system("cls")
                exit()
            elif sure == 'n' or sure == "no" or sure == "0":
                selection()
            else:
                print("Invalid input, choose again...\n")
                time.sleep(2)
                os.system("cls")
                selection()
        else:
            print("Invalid input, choose again...\n")
            time.sleep(2)
            os.system("cls")
            selection()		
        




if __name__ == "__main__":
    initialize() # Essential
    selection() # Essential


















#def folder_hierarchie():    # Builds a custom folder hierarchie in selected path (with tkinter package)
	

#def stitching():    # Opens the stitching method of Fiji
	

#def labkit_segmentation_with_classifier():  # Opens the Labkit "Segment Images in Directory With Labkit"

#def measure_area():     #Automatically opens leaf pictures, measures them and saves measurements in dedicated folder
# 	list = new java.io.File(inputDir).list();

# // Process each image in the directory
# for i in range len(list):
#     // Open the image
#     IJ.run("Open...", "path=[" + inputDir + list[i] + "]")

#     // Set the Wand Tool options
#     //WandToolOptions.setStart(IJ.getImage().getWidth() / 2, IJ.getImage().getHeight() / 2)
#     WandToolOptions.setStart(10, 10)

#     // Select the Wand Tool
#     IJ.setTool("Wand Tool")

#     // Use the Wand Tool
#     IJ.doWand(WandToolOptions.getTolerance(), WandToolOptions.getMode() + (Prefs.smoothWand ? " smooth" : ""))

#     // Create a selection based on the Wand Tool results
#     IJ.run("Make Inverse")

#     // Call the Measure command
#     IJ.run("Measure");

#     IJ.wait(500); // Wait for 500 milliseconds

#def combine_data():     #combines all the data into one tsv





