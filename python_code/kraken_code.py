import os
import subprocess
import kraken  # Kraken OCR

# Path to the directory containing the folders
root_directory = "/media/sau/TRAVAIL/ubuntu-proj/wait"

kraken_model = "/home/sau/sau-project/viefr_best.mlmodel"

# Iterate through each folder in the root directory
for folder_name in os.listdir(root_directory):
    folder_path = os.path.join(root_directory, folder_name)
    
    # Check if the item is a folder
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        

        # Iterate through PNG files in the folder
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith(".png"):
                image_path = os.path.join(folder_path, image_file)
                output_file = os.path.splitext(image_file)[0] + "_output.txt"
                
		# Run Kraken OCR with the specific model using subprocess
                # kraken_cmd = f"kraken -i '{image_path}' -m '{kraken_model}' '{output_file}' binarize segment ocr"
                kraken_cmd = f"kraken -i '{image_path}' '{output_file}' binarize segment ocr -m '{kraken_model}'"
                subprocess.run(kraken_cmd, shell=True, cwd=folder_path)

                print(f"Processed {image_file}. OCR output saved to {output_file}")
                


# print("asfd")