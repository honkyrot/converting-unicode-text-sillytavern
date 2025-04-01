# python script that replaces some unicode characters to it's ascii equivilent
# files are png images with base64 metadata at the end of the image data, we only intend to modify that part only.

# characters targeted : 
# U+201C, U+201D, U+2026, U+2019

# get directory of file
import os
import base64

from PIL import Image
from PIL.PngImagePlugin import PngInfo

affected_files = 0
affected_characters = 0

# if True, will replace unicode characters
write_enabled = True

dir = "D:\\AI LLMs SillyTavern\\SillyTavern\\data\\default-user\\characters"

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
        with open(os.path.join(dir, filename), "r") as f:
            print("\nReading file: " + filename)
            affected_files += 1

            f = open(os.path.join(dir, filename), "rb")
            image = Image.open(f)
            image_metadata = image.text

            # data extracted is a dictionary, chara & ccv3
            char_data = image_metadata["chara"]
            
            decoded_char_bytes = base64.b64decode(char_data)
            decoded_char_data = decoded_char_bytes.decode("utf-8")

            # count characters that are to be replaced
            count = 0
            for char in decoded_char_data:
                if char == "\u201c" or char == "\u201d" or char == "\u2026" or char == "\u2019":
                    count += 1
                    affected_characters += 1

            print("Characters to be replaced: " + str(count))

            # replace unicode characters if wrtie enabled
            if write_enabled:
                decoded_char_data = decoded_char_data.replace("\u201c", '\\"')
                decoded_char_data = decoded_char_data.replace("\u201d", '\\"')
                decoded_char_data = decoded_char_data.replace("\u2026", "...")
                decoded_char_data = decoded_char_data.replace("\u2019", "'")

                # encode to base64
                encoded_char_data = base64.b64encode(decoded_char_data.encode("utf-8")).decode("utf-8")

                # write to file
                print("Writing file: " + filename)

                new_metadata = PngInfo()
                new_metadata.add_text("chara", encoded_char_data)
                new_metadata.add_text("ccv3", encoded_char_data)

                image.save(os.path.join(dir, filename), pnginfo=new_metadata)

            f.close()
            print("Finished file: " + filename)

print("\nTotal affected files: " + str(affected_files))
print("Total affected characters: " + str(affected_characters))
# input("Press enter to exit...")