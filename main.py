# python script that replaces some unicode characters to it's ascii equivilent
# files are png images with base64 metadata at the end of the image data, we only intend to modify that part only.

# this file can read and write to ALL characters

# get directory of file
import os
import operations

affected_files = 0
affected_characters = 0

# if True, will replace unicode characters, otherwise reads total char count
write_enabled = False

# retrieve dir from env
dir = os.getenv("DIR") + "\\data\\default-user\\characters"

total_files = 0
for filename in os.listdir(dir):
    if filename.endswith(".png"):
        total_files += 1

# confirm directory
if write_enabled:
    print("Directory: " + dir)
    print("Warning: You are about to modify " + str(total_files) + " files.")
    print("Continue? (y/n)")

    user_input = input()

    if user_input != "y":
        exit()
else:
    print("Directory: " + dir)
    print("Writing disabled, only reading " + str(total_files) + " files.")

for filename in os.listdir(dir):
    if filename.endswith(".png"):
        a_c = operations.replace_unicode_characters(dir, filename, write_enabled)

        affected_characters += a_c
        affected_files += 1

print("\nTotal affected files: " + str(affected_files))
print("Total affected characters: " + str(affected_characters))
# input("Press enter to exit...")
