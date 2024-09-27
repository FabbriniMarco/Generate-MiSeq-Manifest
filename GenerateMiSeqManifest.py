import os
import sys
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import csv
import shutil

# Helper function to get the correct path to resources
def resource_path(relative_path):
    try:
        # PyInstaller creates a temporary folder and stores files there
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Use the resource_path function to load the external files
index_database_path = resource_path('index_database.tsv')
header_file_path = resource_path('header.tsv')
example_plate_path = resource_path('EXAMPLE_PLATES.xlsx')

# Load preloaded data
index_database = pd.read_csv(index_database_path, sep="\t")

class MiSeqManifestGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("MiSeq Manifest Generator")

        # Set the window icon
        self.root.iconbitmap(resource_path('ICON.ico'))

        # Use ttkbootstrap themes and styles for a better look
        self.style = ttk.Style("darkly")
        
        # Create the layout
        ttk.Label(root, text="Project Name:").grid(row=0, column=0, padx=10, pady=10)
        self.project_name_entry = ttk.Entry(root)
        self.project_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Project Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        self.project_date_entry = ttk.Entry(root)
        self.project_date_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(root, text="Number of Plates:").grid(row=2, column=0, padx=10, pady=10)
        self.n_plates_entry = ttk.Entry(root)
        self.n_plates_entry.grid(row=2, column=1, padx=10, pady=10)

        # Button to select the Excel file
        ttk.Button(root, text="Select Excel File", command=self.select_file).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Button to generate the manifest
        ttk.Button(root, text="Generate Manifest", command=self.generate_manifest, bootstyle=SUCCESS).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Button to get example plate file
        ttk.Button(root, text="Get Example Plate File", command=self.get_example_plate, bootstyle="INFO-OUTLINE").grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        
    def generate_manifest(self):
        project_name = self.project_name_entry.get()
        project_date = self.project_date_entry.get()
        n_plates = self.n_plates_entry.get()

        # Validate inputs
        if not project_name or not project_date or not n_plates or not self.file_path:
            messagebox.showerror("Error", "All fields and the Excel file must be provided!")
            return

        try:
            n_plates = int(n_plates)
            project_date = pd.to_datetime(project_date).strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date or number of plates format.")
            return

        # Ask for output destination
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                initialfile=f"{project_name}_SampleSheet_{project_date}.csv")
        if not output_file:
            messagebox.showerror("Error", "Output destination must be specified!")
            return

        # Process the header file
        try:
            header_lines = self.process_header_file(project_name, project_date)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing header file: {str(e)}")
            return

        # Run the manifest generation logic
        try:
            data_section = self.generate_manifest_logic(project_name, n_plates)
            self.write_manifest(header_lines, data_section, output_file)
            messagebox.showinfo("Success", f"Manifest generated successfully: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_example_plate(self):
        # Ask the user where to save the example plate file
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if save_path:
            # Copy the example file to the user's chosen location
            shutil.copy(example_plate_path, save_path)
            messagebox.showinfo("Success", f"Example plate file saved: {save_path}")

    def process_header_file(self, project_name, project_date):
        # Generate the header lines
        header_lines = [
            ["[Header]", "", "", "", "", "", ""],
            [f"Experiment Name,{project_name}", "", "", "", "", "", ""],
            [f"Date,{project_date}", "", "", "", "", "", ""],
            ["Module,GenerateFASTQ - 3.0.1", "", "", "", "", "", ""],
            ["Workflow,GenerateFASTQ", "", "", "", "", "", ""],
            ["Library Prep Kit,Nextera XT", "", "", "", "", "", ""],
            ["Index Kit,Nextera XT v2 Index Kit Sets A B C D", "", "", "", "", "", ""],
            ["Chemistry,Amplicon", "", "", "", "", "", ""],
            ["[Reads]", "", "", "", "", "", ""],
            ["251", "", "", "", "", "", ""],
            ["251", "", "", "", "", "", ""],
            ["[Settings]", "", "", "", "", "", ""],
            ["adapter,CTGTCTCTTATACACATCT", "", "", "", "", "", ""],
            ["[Data]", "", "", "", "", "", ""]
        ]
        
        return header_lines

    def generate_manifest_logic(self, project_name, n_plates):
        index_set = []
        for n in range(1, n_plates + 1):  # Plates are 1-indexed in Excel, Python uses 0-indexing
            sheet = pd.read_excel(self.file_path, sheet_name=n-1, usecols="A:M", nrows=8)
            index_set.append(sheet.columns[0])
        
        if not all(i in ['A', 'B', 'C', 'D'] for i in index_set):
            raise ValueError("Invalid Index Set in Excel file. Use only A, B, C, D.")
        
        index_correspondence = pd.DataFrame({'plate': range(1, n_plates+1), 'index_set': index_set})
        data_section = pd.DataFrame(columns=["Sample_ID", "Description", "I7_Index_ID", "index", "I5_Index_ID", "index2", "Sample_Project"])

        insert = 0
        for n in range(1, n_plates + 1):
            sheet = pd.read_excel(self.file_path, sheet_name=n-1, usecols="A:M", nrows=8)
            index_column = sheet.columns[1:]
            index_row = sheet.iloc[:, 0]
            
            for row in range(len(index_row)):
                if index_row[row] != "empty":
                    for col in range(1, len(index_column) + 1):
                        if not sheet.columns[col].startswith("empty") and sheet.iloc[row, col] != "empty":
                            data_section.loc[insert] = [
                                sheet.iloc[row, col].replace(" ", ""),
                                sheet.iloc[row, col].replace(" ", ""),
                                index_database.loc[index_database["Index_Name"] == sheet.columns[col], "Sequence"].values[0],
                                f"{index_correspondence.loc[index_correspondence['plate'] == n, 'index_set'].values[0]}-{sheet.columns[col]}",
                                index_database.loc[index_database["Index_Name"] == index_row[row], "Sequence"].values[0],
                                f"{index_correspondence.loc[index_correspondence['plate'] == n, 'index_set'].values[0]}-{index_row[row]}",
                                project_name
                            ]
                            insert += 1
        
        return data_section

    def write_manifest(self, header_lines, data_section, output_file):
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(header_lines)  # Write the header section
            writer.writerow(["Sample_ID", "Description", "I7_Index_ID", "index", "I5_Index_ID", "index2", "Sample_Project"])  # Add the data header row
            writer.writerows(data_section.values)  # Write the data section

# Main execution
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = MiSeqManifestGenerator(root)
    root.mainloop()
