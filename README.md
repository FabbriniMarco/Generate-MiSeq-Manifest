# Generate MiSeq Manifest
### Quickly produce a .csv manifest file to import samples into Illumina MiSeq machine for the sequencing run, starting from 96-well plates of samples with matched index codes


  ## Warning: This script works only with Illumina Nextera XT Index v2 (sets A,B,C and D)  
  
  Before using the script consider looking at the _index_database.tsv_ file to check whether your indexes are included.  
    

## Requirements:
The script requires R to be installed (look at the [Comprehensive R Archive Network](https://cran.r-project.org/) if you don't have R installed)  
The readxl package is required. It can be installed automatically during the first run of the script or manually running the following line of code in R/RStudio:  

```R
install.packages("readxl")
```


## Download the script and the required files  
In order to download the files in this repository you can open your Terminal on MacOS or Linux; or your Powershell on Windows and use the following:

```diff
 git clone https://github.com/FabbriniMarco/Generate-MiSeq-Manifest
```
Or you can click on the green "Code" button on top of this page and select the "Download ZIP" option;  
Or you can download the release .zip file from the [Releases](https://github.com/FabbriniMarco/Generate-MiSeq-Manifest/releases) section


## Tutorial for Linux and MacOS:  

Open your Terminal app and head to the folder containing this script and the plates for the run, using the "cd" command, for example:  

```Bash
cd /User/myusername/Downloads/Generate_MiSeq_CSV-2.6.1
```

If you don't know your PATH you can also type "cd " and drag-and-drop the folder from the Finder/FileExplorer inside the terminal.

Paste this in your Terminal, changing the parameters accordingly  
```Bash
Rscript Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 EXAMPLE_PLATES.xlsx
```

You need to change the "Project_name" accordingly to the name you want to give to the run  
You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted  
You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file  
You need to change the "EXAMPLE_PLATES.xlsx" excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template  
  
  
  
## Tutorial for Windows 10 and Windows 11:
Open your Terminal app or Windows PowerShell by searching for "Terminal" or "Powershell" in your Start menu.  
If you have problem finding your terminal, you cen press the keys Win+R and a "Execute" window sill pop out in the bottom-left screen. Type "powershell" and hit Enter.  
Now head to the folder containing the script and the plates for the run, using the "cd" command. Remember to use single quotes for the path. For example:  

```Powershell
cd 'C:\Users\myusername\Downloads\Generate_MiSeq_CSV-2.6.1\'
```

If you don't know your PATH you can also type "cd " and drag-and-drop the folder from the File Explorer inside the terminal.  

Then, we need to locate your Rscript.exe executable. You can open your File Explorer and head to "This PC", then select "OS C:", then "Program Files" (EN) or "Programmi" (IT) and open the "R" folder. Check which one is the latest version (the highest number) and edit the line of code below (R-4.3.1) in order to execute the appropriate version of R.  
Remember to execute the command below with the commercial & first! Note the use of double quotes for the path to the Rscript.exe executable.  
Note to the IT users: even if your folder is named "Programmi", you still need to type "Program Files" in the path below. Just adjust the R-X.X.X version in the path  

```Powershell
& "C:\Program Files\R\R-4.3.1\bin\Rscript.exe" Generate-MiSeq-Manifest.R index_database.tsv header.tsv Project_name 2023-05-18 4 EXAMPLE_PLATES.xlsx
```  

You need to change the "Project_name" accordingly to the name you want to give to the run  
You need to change the date "2023-05-18" setting the date in which the run WILL BE conducted  
You need to change the number "4" - the one between the date and the excel file - according to the number of plates in the excel file  
You need to change the "EXAMPLE_PLATES.xlsx" excel file with the plates accordingly to the samples and plates you have prepared, sticking to the template  



## Additional details:

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
  * The upper left cell must contain a single letter pointing to the adapter set (A, B, C, D). No spaces, no merged cells.
  * Column names and row names MUST contain index codes (N- in the columns, S- in the rows) OR 'empty'
  * The inner part of the table must contain sample's name. Avoid name starting with numbers or containing special characters
  * In case of an empty cell you MUST fill the cell with the term: _**empty**_

    


## Cite this tool if you want:  



```
@Manual{,
  title = {Generate MiSeq Manifest: Quickly produce a .csv manifest file to import samples into Illumina MiSeq machine},
  author = {Marco Fabbrini},
  year = {2023},
  note = {R package version 2.6.1},
  url = {https://github.com/FabbriniMarco/Generate-MiSeq-Manifest.git},
}
```
