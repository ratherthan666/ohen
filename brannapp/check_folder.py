import os

def check_folder():
    target_dir = "/storage/emulated/0/Documents/Bran"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


if __name__ == "__main__":
    check_folder()