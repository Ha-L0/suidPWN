from git import Repo 
import shutil
import os
import base64

temp_clone_dir = "git_temp"
gtfobins_repo = "https://github.com/GTFOBins/GTFOBins.github.io.git"
binary_folder = "_gtfobins"
gtfobins_base_url = "https://gtfobins.github.io/gtfobins/"
output_filename = "binaries"
output_file_content = ""

def list_files_in_directory(directory):
    try:
        # List all files in the directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return files
    except FileNotFoundError:
        return f"The directory '{directory}' does not exist."

# rm old temp dir and create new one (if it still exists)
try:
    shutil.rmtree(temp_clone_dir)
except:
    pass
os.makedirs(temp_clone_dir, exist_ok=True)

# get gtfobins repository and extract binaries
print("[*] Cloning gtfobins repo to extract binary infos...")
Repo.clone_from(gtfobins_repo, temp_clone_dir)
binary_files = list_files_in_directory(temp_clone_dir + "/" + binary_folder)

# go through binaries, look for suid and extract technique
for binary in binary_files:
    f = open(temp_clone_dir + "/" + binary_folder + "/" + binary, "r")
    temp_binary_content = f.readlines()
    f.close()

    binary_payload = ""
    store = 0
    for line in temp_binary_content:
        binary_payload += line
        if "suid:" in line:
            store = 1
    
    if store == 1:
        payload_write = str(base64.b64encode(binary_payload.encode()))
        payload_write = payload_write[2:len(payload_write)-1]
        output_file_content += binary.split(".")[0] + "," + gtfobins_base_url + binary.split(".")[0] + "," + payload_write + "\n"

# create binary file
f = open("binaries", "w")
f.write(output_file_content)
f.close()

# clean up
print("[*] Cleaning up...")
try:
    shutil.rmtree(temp_clone_dir)
except:
    pass

print("[+] Done.")
