import os
import shutil
import hashlib
import argparse
from tqdm import tqdm


def hash_file(file_path):
    """Generate a SHA-256 hash of a file's contents."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def compare_directories(dir_a, dir_b, dir_c, verbose=False):
    """Compare directories A and B, copy unique files from A to C."""
    print(f"Comparing directory A: {dir_a}")
    print(f"With directory B: {dir_b}")
    print(f"Unique files will be copied to: {dir_c}")

    # Create directory C if it doesn't exist
    if not os.path.exists(dir_c):
        os.makedirs(dir_c)

    unique_files = []  # List to store files present in A but not in B
    total_files_a = 0

    # Create a dictionary to store file hashes from directory B
    b_file_hashes = {}

    print("Building file index for directory B...")
    # First pass: Build an index of all files in B by their content hash
    for root, _, files in os.walk(dir_b):
        for file in tqdm(files, desc="Indexing directory B", unit="file"):
            file_b_path = os.path.join(root, file)
            try:
                # Get file size and hash
                file_size = os.path.getsize(file_b_path)
                file_hash = hash_file(file_b_path)
                # Store in dictionary with size and hash as key
                key = (file_size, file_hash)
                if key not in b_file_hashes:
                    b_file_hashes[key] = []
                b_file_hashes[key].append(file_b_path)
            except Exception as e:
                if verbose:
                    print(f"[ERROR] Error processing file {file_b_path}: {e}")

    # Count total files in A for progress bar
    for root, _, files in os.walk(dir_a):
        total_files_a += len(files)

    print(f"Total files in directory A: {total_files_a}")

    # Second pass: Check each file in A against the index from B
    with tqdm(total=total_files_a, desc="Comparing Files", unit="file") as pbar:
        for root, _, files in os.walk(dir_a):
            for file in files:
                file_a_path = os.path.join(root, file)

                try:
                    # Get file size and hash
                    file_size = os.path.getsize(file_a_path)
                    file_hash = hash_file(file_a_path)
                    key = (file_size, file_hash)

                    # Check if this file exists in B by content
                    if key not in b_file_hashes:
                        unique_files.append(file_a_path)
                        if verbose:
                            print(f"[INFO] {file_a_path}: No matching content found in directory B. Marked as unique.")
                    else:
                        if verbose:
                            print(f"[INFO] {file_a_path}: Content matches with file(s) in directory B.")
                except Exception as e:
                    if verbose:
                        print(f"[ERROR] Error processing file {file_a_path}: {e}")

                pbar.update(1)

    if not unique_files:
        print("No unique files found. All files in A have matching content in B.")
        return

    # Copy unique files to directory C
    print(f"Found {len(unique_files)} unique files to copy to directory C")

    # Progress bar for copying unique files
    with tqdm(total=len(unique_files), desc="Copying Files", unit="file") as pbar:
        for file_a_path in unique_files:
            rel_path = os.path.relpath(file_a_path, dir_a)
            target_path = os.path.join(dir_c, rel_path)

            try:
                # Create directory structure if it doesn't exist
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                # Copy file without metadata
                shutil.copyfile(file_a_path, target_path)
                if verbose:
                    print(f"[INFO] {file_a_path}: Copied to {target_path}.")
            except Exception as e:
                print(f"[ERROR] Error copying {file_a_path} to {target_path}: {e}")

            pbar.update(1)

    # Summary report
    print("\nSummary Report:")
    print(f"Total files in directory A: {total_files_a}")
    print(f"Total unique files copied to C: {len(unique_files)}")


def main():
    parser = argparse.ArgumentParser(description='Compare directories A and B, copy unique files from A to C.')
    parser.add_argument('dir_a', help='Path to directory A')
    parser.add_argument('dir_b', help='Path to directory B')
    parser.add_argument('dir_c', help='Path to directory C (where unique files will be copied)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    compare_directories(args.dir_a, args.dir_b, args.dir_c, args.verbose)


if __name__ == '__main__':
    main()
