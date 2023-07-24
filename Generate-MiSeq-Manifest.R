############### script for generating input manifest for MiSeq sequencing machine ##################
# Marco Fabbrini
# VERSION:2.6.1
# RELEASE:24/Lug/2023

args<-commandArgs(TRUE) 


#----------LOAD FILES AND PARAMETERS------
if (!requireNamespace("readxl", quietly = TRUE))
  install.packages("readxl", repos = "https://cran.rstudio.com/")
library(readxl)

# Debugging purposes:
# pDataFile1 <- "index_database.tsv"
pDataFile1 <- args[1]
index_database<- read.delim(pDataFile1, header=T, sep="\t")

# Debugging purposes:
# pDataFile2 <-  "header.tsv"
pDataFile2 <- args[2]
header_table <- read.delim(pDataFile2, header=F, sep="\t")[ , c(1:8)]
header_table$V2[header_table$V2 == ""]=NA
header_table[is.na(header_table)] = ""
header_table = header_table[,c(1:7)]

# Debugging purposes:
# project_name = "test"
# project_date = Sys.Date()+1
project_name = args[3]
project_date = args[4]

header_table$V2[2] = project_name
header_table$V2[3] = project_date

n_plates <- args[5]

pDataFile3 <- args[6]


# SCRIPT ------------------------------------------------------------------

index_set <- c()
for ( n in 1:n_plates)
{
  suppressMessages(assign(paste("plate", n, sep=""), as.data.frame(read_xlsx(path = pDataFile3, sheet = n )[c(1:8),c(1:13)]) ))
  index_set <- c(index_set, colnames(get(paste("plate", n, sep="")))[1] )
}

index_correspondence = data.frame(plate=1:n_plates, index_set=index_set)
data_section = data.frame(matrix(ncol=7))
colnames(data_section) = c("Sample_ID",	"Description"	,"I7_Index_ID",	"index",	"I5_Index_ID",	"index2",	"Sample_Project")
data_section_header = c("Sample_ID",	"Description"	,"I7_Index_ID",	"index",	"I5_Index_ID",	"index2",	"Sample_Project")


# Check for unknown headers -----------------------------------------------
for ( n in 1:n_plates)
{
  if ( ! all ( colnames(get(paste("plate", n, sep="")))[2:13] %in% index_database$Index_Name | grepl("empty", colnames(get(paste("plate", n, sep="")))[2:13]) ) )
  {
    print(paste("No sample sheet has been produced. Check your EXCEL plate table first. Aligator."))
    stop( print( paste("Invalid Index name found in columns of plate N.", n, " --- Index \'", 
                       colnames(get(paste("plate", n, sep="")))[2:13][!(colnames(get(paste("plate", n, sep="")))[2:13] %in% index_database$Index_Name | grepl("empty", colnames(get(paste("plate", n, sep="")))[2:13]))],
                       "\' not found in index_database.tsv", sep="") ) )
  }
  if ( !all( get(paste("plate", n, sep=""))[,1] %in% c(index_database$Index_Name, "empty")  ) )
  {
    print(paste("No sample sheet has been produced. Check your EXCEL plate table first. Aligator."))
    stop( print( paste("Invalid Index name found in rows of plate N. ", n, " --- Index \'", 
                       get(paste("plate", n, sep=""))[,1][!get(paste("plate", n, sep=""))[,1] %in% c(index_database$Index_Name, "empty")],
                       "\' not found", sep="") ) )
  }
}


# Generate the manifest ---------------------------------------------------
insert = 1
for ( n in 1:n_plates)
{
  index_column = colnames(get(paste("plate", n, sep="")))[2:ncol(get(paste("plate", n, sep="")))]
  index_row = get(paste("plate", n, sep=""))[,1]
  for ( row in 1:length(index_row) )
  {
    if ( get(paste("plate", n, sep=""))[row,1] != "empty" ) # If the row Index is "empty" skip all the row
    {
      for ( col in 2:(length(index_column)+1) )
      {
        if ( !grepl("empty", colnames(get(paste("plate", n, sep="")))[col]) ) # If the column Index is "empty" skip all the column
        {
          if ( get(paste("plate", n, sep=""))[row,col] != "empty" ) # If the cell value is "empty" skip it
          {
            data_section[insert,"Sample_ID"] = gsub(" ", "", get(paste("plate", n, sep=""))[row,col])
            data_section[insert,"Description"] = gsub(" ", "", get(paste("plate", n, sep=""))[row,col])
            data_section[insert,"index"] = paste( index_correspondence[index_correspondence$plate == n , "index_set"] ,
                                                  colnames( get(paste("plate", n, sep="")) )[col] , 
                                                  sep="-")
            data_section[insert,"I7_Index_ID"] = index_database[ index_database$Index_Name == colnames( get(paste("plate", n, sep="")) )[col] , "Sequence"]
            data_section[insert,"index2"] = paste( index_correspondence[index_correspondence$plate == n , "index_set"] ,
                                                   get(paste("plate", n, sep=""))[,1][row] , 
                                                   sep="-")
            data_section[insert,"I5_Index_ID"] = index_database[ index_database$Index_Name == get(paste("plate", n, sep=""))[,1][row] , "Sequence"]
            data_section[insert,"Sample_Project"] = project_name
            insert = insert + 1
          }
        }
      }
    }
  }
}


# Check for weird sample names --------------------------------------------
if ( ( length( grep(" ", data_section$Sample_ID) ) + length( grep("\\.", data_section$Sample_ID) ) ) != 0  ) {
  print(paste("I strongly suggest you to check your samples name"))
  print(paste("Golden rule for assigning good sample's names:"))
  print(paste("• Don't start any name with a number"))
  print(paste("• Avoid using spaces, points or special characters such as * ' / + ° #, etc..."))
  print(paste("• It's better to use names indicative of sample's characteristics (e.g., with timepoint and/or group, treatment or whatever)"))
}


# Check for duplicated samples --------------------------------------------
if ( any(duplicated(data_section$Sample_ID)) )
{
  qualeduplicato = data_section$Sample_ID[duplicated(data_section$Sample_ID)]
  for ( n in 1:n_plates )
  {
    for ( dupiter in qualeduplicato)
    {
      if ( any(grepl(dupiter, get(paste("plate", n, sep="")))) )
      {
        posizione_colonne = grep(dupiter, get(paste("plate", n, sep="")))
        for ( quantidup in 1:length(posizione_colonne) )
        {
          colonna_temp = LETTERS[posizione_colonne[quantidup]]
          riga_temp = 1+ which( get(paste("plate", n, sep=""))[,posizione_colonne[quantidup]] == dupiter )
          print( paste("Duplicate ", dupiter , " found in plate N.", n, ", index set ", index_correspondence$index_set[index_correspondence$plate == n], ", EXCEL coordinates ", colonna_temp,  riga_temp, sep=""))
        }
      }
    }
  }
  
  print(paste("No sample sheet has been produced. Check your EXCEL plate table first. Aligator."))
} else {
  colnames(data_section) = colnames(header_table)
  final_format <- rbind(header_table, data_section_header, data_section)
  # If everything is fine, save the manifest to a CSV file, ready for the sequencer
  write.table( final_format, paste(project_name, "_SampleSheet_", project_date, ".csv", sep=""), sep=",", col.names=F, row.names=F, quote=F)
  print(paste("Manifest generated succesfully"))
}


######################################-
