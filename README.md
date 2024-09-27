<div align=center>
  <img width="196" alt="Circle logo" src="https://github.com/user-attachments/assets/4e9887af-3bd1-4a20-bfa6-dd3f73f04da6" height="186">
</div>

# Generate-MiSeq-Manifest
Quickly produce a .csv manifest file to import samples into Illumina MiSeq machine for the sequencing run, starting from 96-well plates of samples with matched index codes

### Warning: This script works only with Illumina Nextera XT Index v2 (sets A,B,C and D)  
  
If you are unsure about the index sequence you are using, consult the manufacturer of your library prep kits and check the ```index_database.tsv```.  
    
<br>


## Table of contents
1. [GUI program portables](#gui-program-portables)
   - [Windows 10/11 users](#windows-users)
   - [MacOS users](#macos-users)
2. [Run the GUI from command line](#run-the-gui-from-cli-windows-macos-linux)
3. [Run the legacy Rscript](#run-the-legacy-rscript)
   - [Requirements](#requirements)
   - [Download the script and the required files](#download-the-script-and-the-required-files)
   - [Legacy CLI execution for Linux and MacOS](#legacy-cli-execution-for-linux-and-macos)
   - [Legacy CLI execution for Windows 10/11](#legacy-cli-execution-for-windows)
   - [Additional details for the legacy CLI](#additional-details-for-the-legacy-cli)
4. [Citation](#citation)

<br>
<br>


# GUI program portables
## Windows users
[Download the ```.exe``` executable](https://github.com/FabbriniMarco/Generate-MiSeq-Manifest/releases/download/v2.7/GenerateMiSeqManifest.exe) in the Release section of this repo.
Simply double click the executable. You will get a warning as the executable file is not signed, but you can proceed and a GUI as follows will appear:

<div align=center>
  <img width="396" alt="GUI example" src="https://github.com/user-attachments/assets/6da3fe5e-50e7-4028-9008-df54e9b28522" height="360">
</div>

You can click the ```Get Example Plate File``` button at the bottom and point a place where save the EXAMPLE_PLATES.xlsx file. This is a template excel file with the plates, that you can fill in accordingly to the samples and plates you have prepared, sticking to the template.
After compiling the text box fields ```Project Name```, ```Project Date``` in YEAR-MONTH-DAY format and ```Number of Plates``` you have to provide the excel file in the prompt that opens when clicking the ```Select Excel File``` and you're good to go! Just press the ```Generate Manifest``` and specify an output directory where to save your sample sheet for the sequencing run.

<br>

## MacOS users
MacOS users can [download the ```.app```](https://github.com/FabbriniMarco/Generate-MiSeq-Manifest/releases/download/v2.7/GenerateMiSeqManifest-MacOS-arm.zip) in the ZIP archive in the Release section of this repo. The program should work on MacOS with ARM processors (M!, M2, M3) but has not been tested. Please raise any Issue through the Issue section of this repo.
<br> Alternatively MacOS user can run the .py script from the Terminal (see next section).
***

<br>
<br>

# Run the GUI from CLI (Windows, MacOS, Linux):
The script requires a valid ```python``` installation as well as several dependancies libraries. Then, clone this repo and launch the python script locally.

```bash
pip install pandas tk ttkbootstrap

git clone https://github.com/FabbriniMarco/Generate-MiSeq-Manifest

cd Generate-MiSeq-Manifest

python ./GenerateMiSeqManifest.py
```
***

<br>
<br>


# Run the legacy Rscript
If you want to run the legacy Rscript you can. It has been moved inside the  [Legacy R Script](https://github.com/FabbriniMarco/Generate-MiSeq-Manifest/tree/main/Legacy%20R%20script) folder of this repo. <br>

## Requirements
The legacy version of this script requires R to be installed (look at the [Comprehensive R Archive Network](https://cran.r-project.org/) if you don't have R installed)  
The readxl package is required. It can be installed automatically during the first run of the script or manually running the following line of code in R/RStudio:  

```R
install.packages("readxl")
```

<br>

## Download the script and the required files  
In order to download the files in this repository you can open your Terminal on MacOS or Linux; or your Powershell on Windows and use the following:

```diff
 git clone https://github.com/FabbriniMarco/Generate-MiSeq-Manifest
```
Or you can click on the green "Code" button on top of this page and select the "Download ZIP" option;  
Or you can download the release .zip file from the [Releases](https://github.com/FabbriniMarco/Generate-MiSeq-Manifest/releases) section

<br>

## Legacy CLI execution for Linux and MacOS  

Open your Terminal app and head to the folder containing this script and the plates for the run, using the "cd" command, for example:  

```bash
cd /User/myusername/Downloads/Generate_MiSeq_CSV-2.7
```

If you don't know your PATH you can also type ```cd ``` and drag-and-drop the folder from the Finder/FileExplorer inside the terminal.

Paste this in your Terminal, changing the parameters accordingly  
```bash
Rscript Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 EXAMPLE_PLATES.xlsx
```

You need to change the "Project_name" accordingly to the name you want to give to the run  
You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted  
You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file  
You need to change the "EXAMPLE_PLATES.xlsx" excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template  
  
<br>

  
## Legacy CLI execution for Windows
Open your Terminal app or Windows PowerShell by searching for "Terminal" or "Powershell" in your Start menu.  
If you have problem finding your terminal, you can press the keys Win+R and a "Execute" window will pop out in the bottom-left screen. Type "powershell" and hit Enter.  
Now head to the folder containing the script and the plates for the run, using the "cd" command. Remember to use single quotes for the path. For example:  

```Powershell
cd 'C:\Users\myusername\Downloads\Generate_MiSeq_CSV-2.7\'
```

If you don't know your PATH you can also type "cd " and drag-and-drop the folder from the File Explorer inside the terminal.  

Then, we need to locate your Rscript.exe executable. You can open your File Explorer and head to "This PC", then select "OS C:", then "Program Files" (EN) or "Programmi" (IT) and open the "R" folder. Check which one is the latest version (the highest number) and edit the line of code below (R-4.3.1) in order to execute the appropriate version of R.  
Remember to execute the command below with the commercial & first! Note the use of double quotes for the path to the Rscript.exe executable.  
Note to the Italian users: even if your folder is named "Programmi", you must type "Program Files" in the path below. Just adjust the R-X.X.X version in the path  

```Powershell
& "C:\Program Files\R\R-4.3.1\bin\Rscript.exe" Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 EXAMPLE_PLATES.xlsx
```  

You need to change the "Project_name" accordingly to the name you want to give to the run  
You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted  
You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file  
You need to change the "EXAMPLE_PLATES.xlsx" excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template  


<br>

## Additional details for the legacy CLI

* Items meaning:
  * 1st argument contains the index database supplied
  * 2nd argument contains the header section supplied
  * 3rd argument specifies the project name. MUST avoid using spaces or special characters (e.g., wildcards . * )
  * 4th argument specifies the project's date. MUST use the date of the sequencing run in format YYYY-MM-DD
  * 5th argument contains the number of plates present in the XLSX file
  * 6th argument pointss to the XLSX file for the plates built as such:
* Things to check:
  * Each separate plate is in a separate sheet
  * The plate must start from the first cell in the upper left corner of the Excel sheet
  * The upper left cell must contain a single letter pointing to the adapter set (A, B, C, D). No spaces, no merged cells
  * Column names and row names MUST contain index codes (N- in the columns, S- in the rows) OR 'empty'
  * The inner part of the table must contain sample's name. Avoid name starting with numbers or containing special characters
  * In case of an empty cell you MUST fill the cell with the term: _**empty**_
***
    
<br>
<br>

***
## Citation
If you use this tool please cite: <br>

```
@Manual{,
  title = {Generate-MiSeq-Manifest: Quickly produce a .csv manifest file to import samples into Illumina MiSeq machine},
  author = {Marco Fabbrini},
  year = {2023},
  note = {version 2.7},
  url = {https://github.com/FabbriniMarco/Generate-MiSeq-Manifest.git},
}
```
