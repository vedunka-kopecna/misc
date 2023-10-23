import os
import sys
import shutil
import hashlib
from datetime import datetime
import time

def synchronize_folders(source_folder, replica_folder, log_file, interval):
    """
    Synchronizes a source folder with its replica periodically in the given time interval.

    :param source_folder: folder which the user wants to back up
    :param replica_folder: folder representing the copy of the source one
    :param log_file: logging of changes while synchronizing
    :param interval: how often synchronization is performed
    :return: an exact copy of the source folder
    """
    while True:
        print("Synchronization started, to stop press Ctrl+C")
        # Create replica folder if it doesn't already exist
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        # Get a list of files in the source folder
        source_files = set(os.listdir(source_folder))

        # Get a list of files in the replica folder
        replica_files = set(os.listdir(replica_folder))

        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, 'a') as log:
            log.write(f"{current_datetime} - Synchronization started.\n")

            # Copy new or modified files from source to replica
            for file_name in source_files:
                source_path = os.path.join(source_folder, file_name)
                replica_path = os.path.join(replica_folder, file_name)

                if file_name not in replica_files or not are_files_identical(source_path, replica_path):
                    shutil.copy2(source_path, replica_path)
                    log.write(f"Copied: {file_name}\n")

            # Remove files from replica that are not in source
            for file_name in replica_files - source_files:
                file_path = os.path.join(replica_folder, file_name)
                os.remove(file_path)
                log.write(f"Removed: {file_name}\n")

        # Sleep interval to control synchronization frequency
        time.sleep(interval)


def are_files_identical(file1, file2):
    # Check if two files are identical based on MD5 hash
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    return hash1 == hash2


def hash_file(file_path):
    # Calculate the MD5 hash of a file
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python sync_folders.py <source_folder> <replica_folder> <log_file> <interval in seconds>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]
    sync_interval = float(sys.argv[4])

    synchronize_folders(source_folder, replica_folder, log_file, sync_interval)