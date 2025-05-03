import os
import shutil
import datetime
from pathlib import Path
import sys
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
import mimetypes
import logging

# Configure logging for UTF-8 encoding


def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(message)s')

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler("organize_files.log", encoding='utf-8')
    file_handler.setFormatter(log_formatter)

    # Stream handler with UTF-8 encoding
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, stream_handler]
    )


# Call setup_logging to configure logging
setup_logging()


def get_date_taken(file_path):
    try:
        with Image.open(file_path) as image:
            # Check for PNG specifically known for issues
            if isinstance(image, Image.Image) and image.format == 'PNG':
                logging.info(f"Handling PNG file: {file_path}")

            # Handle JPG or other image types
            if hasattr(image, '_getexif'):
                exif_data = image._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in ('DateTimeOriginal', 'DateTime'):
                            date_str = value.split()[0]
                            return datetime.datetime.strptime(date_str, '%Y:%m:%d').year
            logging.info(f"No EXIF data found in {file_path}, using file timestamps.")

    except UnidentifiedImageError:
        logging.warning(f"Cannot identify image file (may be corrupt) {file_path}. Using file timestamps.")
    except Exception as e:
        logging.warning(f"Error extracting EXIF data from {file_path}. Using file timestamps. Error: {e}")

    # Fallback: Use file modified date
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).year
    except Exception as e:
        logging.error(f"Failed to get file timestamp for {file_path}. Error: {e}")
        return None


def organize_files_by_year(source_dir, dest_dir):
    try:
        os.makedirs(dest_dir, exist_ok=True)

        # Create the Problematic_Files directory
        problem_dir = os.path.join(dest_dir, "Problematic_Files")
        os.makedirs(problem_dir, exist_ok=True)

        for root, _, files in os.walk(source_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                try:
                    mime_type, _ = mimetypes.guess_type(file_path)

                    # Process image files
                    if mime_type and mime_type.startswith('image'):
                        year = get_date_taken(file_path)

                        if year:
                            rel_path = os.path.relpath(root, source_dir)
                            new_folder_path = os.path.join(dest_dir, str(year), rel_path)
                            os.makedirs(new_folder_path, exist_ok=True)
                            try:
                                shutil.copy2(file_path, new_folder_path)
                                logging.info(f"Copied {file_name} to {new_folder_path}")
                            except Exception as e:
                                logging.error(f"Failed to copy {file_path}. Error: {e}")
                        else:
                            logging.warning(f"No valid date found for {file_path}, copying to problem directory.")
                            copy_to_problem_dir(file_path, root, source_dir, problem_dir)

                    # Process non-image files
                    else:
                        year = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).year
                        if year:
                            rel_path = os.path.relpath(root, source_dir)
                            new_folder_path = os.path.join(dest_dir, str(year), rel_path)
                            os.makedirs(new_folder_path, exist_ok=True)
                            shutil.copy2(file_path, new_folder_path)
                            logging.info(f"Copied {file_name} to {new_folder_path}")

                except Exception as e:
                    logging.error(f"Error processing file {file_name}. Error: {e}")
                    copy_to_problem_dir(file_path, root, source_dir, problem_dir)

    except Exception as e:
        logging.critical(f"An error occurred while organizing files. Error: {e}")


def copy_to_problem_dir(file_path, root, source_dir, problem_dir):
    try:
        rel_path = os.path.relpath(root, source_dir)
        problem_folder_path = os.path.join(problem_dir, rel_path)
        os.makedirs(problem_folder_path, exist_ok=True)
        shutil.copy2(file_path, problem_folder_path)
        logging.info(f"Copied problematic file {file_path} to {problem_folder_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path} to problem directory. Error: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python organize_files.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_dir = Path(sys.argv[1]).resolve()
    dest_dir = Path(sys.argv[2]).resolve()

    if not source_dir.exists():
        print(f"Source directory {source_dir} does not exist.")
        sys.exit(1)

    organize_files_by_year(source_dir, dest_dir)


if __name__ == '__main__':
    main()
