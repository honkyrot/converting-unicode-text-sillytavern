# the operations module

import os
import base64

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

# characters targeted : 
# U+201C, U+201D, U+2026, U+2019, U+2018

# function to replace unicode characters
def replace_unicode_characters(dir, selected_file, write_enabled):
    affected_characters = 0

    with open(os.path.join(dir, selected_file), "r") as f:
        print("\nReading file: " + selected_file)

        f = open(os.path.join(dir, selected_file), "rb")
        image = Image.open(f)
        image_metadata = image.text

        # data extracted is a dictionary, chara & ccv3
        char_data = image_metadata["chara"]
        
        decoded_char_bytes = base64.b64decode(char_data)
        decoded_char_data = decoded_char_bytes.decode("utf-8")

        # count characters that are to be replaced
        count = 0
        for char in decoded_char_data:
            if char == "\u201c" or char == "\u201d" or char == "\u2026" or char == "\u2019" or char == "\u2018":
                count += 1
                affected_characters += 1

        print("Characters to be replaced: " + str(count))

        # replace unicode characters if wrtie enabled
        if write_enabled:
            decoded_char_data = decoded_char_data.replace("\u201c", '\\"')
            decoded_char_data = decoded_char_data.replace("\u201d", '\\"')
            decoded_char_data = decoded_char_data.replace("\u2026", "...")
            decoded_char_data = decoded_char_data.replace("\u2019", "'")
            decoded_char_data = decoded_char_data.replace("\u2018", "'")

            # encode to base64
            encoded_char_data = base64.b64encode(decoded_char_data.encode("utf-8")).decode("utf-8")

            # write to file
            print("Writing file: " + selected_file)

            new_metadata = PngInfo()
            new_metadata.add_text("chara", encoded_char_data)
            new_metadata.add_text("ccv3", encoded_char_data)

            try:
                image.save(os.path.join(dir, selected_file), pnginfo=new_metadata)
            except:
                print("Failed to write file: " + selected_file)

            print("Finished writing file: " + selected_file)

        f.close()
    
    return affected_characters