# manage-pictures-repo

## organize_files.py

**Overview**

This script organizes photos and other files into a directory structure based on the year they were taken or created. It preserves the original folder structure within each year folder, making it easy to browse your media chronologically while maintaining your original organization.

**Features**

- **Year-Based Organization**: Automatically sorts files into folders by year (2015, 2016, etc.)
- **EXIF Data Extraction**: Reads date information from image metadata when available
- **Fallback to File Timestamps**: Uses file creation/modification dates when EXIF data isn't available
- **Structure Preservation**: Maintains original subfolder organization within each year
- **Problem File Handling**: Places files with issues in a separate "Problematic_Files" directory
- **Comprehensive Logging**: Detailed logs of all operations with UTF-8 support

**Requirements**

- Python 3.6 or higher

Install the required package using:

```bash
python -m venv .venv
.\.venv\Scripts\activate (or source .venv/bin/activate on MacOS)
pip install -r .\requirements.txt
```

**Usage**

```bash
python organize_files.py <source_directory> <destination_directory>
```

Arguments

- source_directory: Path to the folder containing your photos and other files
- destination_directory: Path where the organized folder structure will be created

**How It Works**

1. Scanning: The script scans all files in the source directory and its subfolders
2. Date Extraction:

- For images: Extracts the date from EXIF metadata when available
- For other files: Uses the file's modification date

3. Organization: Creates a year-based folder structure in the destination directory
4. Copying: Copies files to their appropriate year folders while preserving the original subfolder structure
5. Problem Handling: Files that can't be processed properly are copied to a "Problematic_Files" directory

**Example**

```bash
python organize_files.py C:\Users\Photos D:\Organized_Photos
```

This will:

1. Scan all files in C:\Users\Photos
2. Create year folders (2015, 2016, etc.) in D:\Organized_Photos
3. Copy files to the appropriate year folders based on when they were taken/created
4. Preserve the original subfolder structure within each year folder

**Notes**

- The script creates a log file (organize_files.log) in the current directory
- The script does not modify or delete any files in the source directory
- Special handling is included for PNG files and other potentially problematic formats

**Troubleshooting**

If you encounter issues:

- Check the log file for detailed information about any errors
- Make sure you have read access to the source directory and write access to the destination
- Ensure the Pillow library is properly installed

## compare_directories.py

A brief description of what this project does and who it's for

**Overview**

This script compares two directories (A and B) and identifies files in directory A that don't exist in directory B based on their content. It then copies these unique files to a third directory (C) while preserving the original folder structure from directory A.

**Features**

- **Content-Based Comparison**: Identifies unique files based on their content, not just file names
- **Metadata-Independent**: Ignores file metadata like creation dates and modification times
- **Structure Preservation**: Maintains the original folder structure when copying files
- **Progress Tracking**: Shows progress bars for both indexing and copying operations
- **Detailed Reporting**: Provides a summary of files processed and copied
- **Verbose Mode**: Optional detailed logging about why files are considered unique

**Requirements**

- Python 3.6 or higher

Install the required package using:

```bash
python -m venv .venv
.\.venv\Scripts\activate (or source .venv/bin/activate on MacOS)
pip install -r .\requirements.txt
```

**Usage**

```bash
python compare_directories.py /path/to/directory/A /path/to/directory/B /path/to/directory/C [-v]
```

Arguments

- dir_a: Path to the source directory (directory A)
- dir_b: Path to the reference directory (directory B)
- dir_c: Path to the destination directory (directory C) where unique files will be copied
- -v, --verbose: Enable verbose output (optional)

**How It Works**

1. Indexing: The script first builds an index of all files in directory B based on their size and content hash
2. Comparison: Each file in directory A is checked against this index to determine if it's unique
3. Copying: Files from directory A that don't have matching content in directory B are copied to directory C

**Example**

```bash
python compare_directories.py /home/user/photos /home/user/backup /home/user/unique_photos -v
```

This command will:

1. Compare all files in /home/user/photos with files in /home/user/backup
2. Copy any files that exist only in /home/user/photos to /home/user/unique_photos
3. Preserve the original folder structure from /home/user/photos
4. Show detailed information about the comparison process

**Notes**

- The script uses SHA-256 hashing to compare file contents
- The indexing is stored in memory during script execution
- Large directories may require significant memory for the indexing process
- Files are copied without their original metadata

**Troubleshooting**

If you're seeing more unique files than expected:

- Use the -v flag to see detailed information about why files are considered unique
- Check if the files actually have different content (they might look the same but have different data)
- Ensure both directories are accessible and readable
