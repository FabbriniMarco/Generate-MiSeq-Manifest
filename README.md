###############------ Help section: script for generating input manifest for MiSeq sequencing machine------##################
# Marco Fabbrini
# VERSION:2.6.1
# RELEASE:24/Lug/2023

# Requirements:
# # The readxl package is required ( install.packages("readxl") in a R session)
# # Rscript bash bin is required (on MacOS or Linux platforms), or either use the Rscript.exe windows executable

###### ---------
###### Tutorial for Linux and MacOS:
# Open your Terminal app and head to the folder containing this script and the plates for the run, using the "cd" command, for example:
cd /User/myusername/Downloads/Generate_MiSeq_CSV-2.6.1
# If you don't know your PATH you can also type "cd " and drag-and-drop the folder from the Finder/FileExplorer inside the terminal.

# Paste this in your Terminal, changing the parameters accordingly
Rscript Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 ESEMPIO_PLATE.xlsx

## You need to change the "Project_name" accordingly to the name you want to give to the run
## You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted
## You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file
## You need to change the excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template


###### ---------
###### Tutorial for Windows 10 and Windows 11:
# Open your Terminal app or Windows PowerShell by searching for "Terminal" or "Powershell" in your Start menu
# If you have problem finding your terminal, you cen press the keys Win+R and a "Execute" window sill pop out in the bottom-left screen. Type "powershell" and hit Enter. 
# Now head to the folder containing the script and the plates for the run, using the "cd" command. Remember to use single quotes for the path. For example:
cd 'C:\Users\myusername\Downloads\Generate_MiSeq_CSV-2.6.1\'

# If you don't know your PATH you can also type "cd " and drag-and-drop the folder from the File Explorer inside the terminal.

# Then, we need to locate your Rscript.exe executable. You can open your File Explorer and head to "This PC", then select "OS C:", then "Program Files" (EN) or "Programmi" (IT) and open the "R" folder. Check which one is the latest version (the highest number) and edit the line of code below (R-4.3.1) in order to execute the appropriate version of R.
# Remember to execute the command below with the commercial & first! Note the use of double quotes for the path to the Rscript.exe executable.
# Note to the IT users: even if your folder is named "Programmi", you still need to type "Program Files" in the path below. Just adjust the R-X.X.X version in the path

& "C:\Program Files\R\R-4.3.1\bin\Rscript.exe" Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 ESEMPIO_PLATE.xlsx

## You need to change the "Project_name" accordingly to the name you want to give to the run
## You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted
## You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file
## You need to change the excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template



# Additional details:

# 1st argument contains the index database supplied
# 2nd argument contains the header section supplied
# 3rd argument specifies the project name. MUST avoid using spaces or special characters (e.g., wildcards . * )
# 4th argument specifies the project's date. MUST use the date of the sequencing run in format YYYY-MM-DD
# 5th argument contains the number of plates present in the XLSX file
# 6th argument pointss to the XLSX file for the plates built as such:
# # Each separate plate is in a separate sheet
# # The plate must start from the first cell in the upper left corner of the Excel sheet
# # The upper left cell must contain a single letter pointing to the adapter set (A, B, C, D). No spaces, no merged cells.
# # Column names and row names MUST contain index codes (N- in the columns, S- in the rows) OR 'empty'
# # The inner part of the table must contain sample's name. Avoid name starting with numbers or containing special characters
# # In case of an empty cell you MUST fill the cell with the term: 'empty'
# # An example of a plate file is supplied
