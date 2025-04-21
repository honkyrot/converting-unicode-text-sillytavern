# python script that replaces some unicode characters to it's ascii equivilent
# use main.py to replace all
# this variant is for searching and affecting the specific character

# files are png images with base64 metadata at the end of the image data, we only intend to modify that part only.

# get directory of file
import os
import operations

from PIL import Image
from PIL.PngImagePlugin import PngInfo

# if True, will replace unicode characters
write_enabled = True

dir = "D:\\AI LLMs SillyTavern\\SillyTavern\\data\\default-user\\characters"

total_files = 0
for filename in os.listdir(dir):
    if filename.endswith(".png"):
        total_files += 1

print("Total files: " + str(total_files))

# file search

while True:
    filename = input("\nSearch for: ")
    # index files that contain filename
    l_filename = filename.lower() # for case insensitive
    file_index = 0
    index = []

    selected_file = None

    # get files
    for files in os.listdir(dir):
        if l_filename in str(files).lower():
            print(f"[{file_index}]: {files}")
            file_index += 1
            index.append(files)

    # select file
    if len(index) > 0:
        print("\nFound " + str(len(index)) + " files.")
        cancel = False

        while True:
            try:
                file_index = int(input("Select file index, type -1 to cancel: "))

                if file_index == -1:
                    cancel = True
                    break

                selected_file = index[file_index]
                break
            except:
                print("Invalid index, please try again.")

        if cancel:
            continue

        # open file
        operations.replace_unicode_characters(dir, selected_file, write_enabled)

    else:
        print("No files found, please refine your search.")
