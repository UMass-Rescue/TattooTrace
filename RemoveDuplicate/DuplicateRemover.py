from PIL import Image
import imagehash
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor


class DuplicateRemover:
    def __init__(self, dirname, hash_size=8):
        self.dirname = dirname
        self.hash_size = hash_size

    def _generate_hash(self, filename):
        """Generates a hash for an image, resizing it to reduce processing time."""
        with Image.open(filename) as img:
            # Resize the image using Image.Resampling.LANCZOS for better quality
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            return imagehash.average_hash(img, self.hash_size), filename
       

    
    def find_similar(self, similarity=80):
        """Finds and optionally deletes similar images based on the specified similarity threshold."""
        fnames = [os.path.join(self.dirname, f) for f in os.listdir(self.dirname) if not f.startswith('.')]
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (self.hash_size ** 2))

        # Use a dictionary to store image hashes for quick lookups
        hashes = {}
        # Use a set to keep track of unique images marked for potential deletion
        unique_similars = set()

        print("Generating hashes...")
        with ThreadPoolExecutor() as executor:
            for img_hash, filename in executor.map(self._generate_hash, fnames):
                hashes[filename] = img_hash

        print("Finding Similar Images Now!\n")
        for base_fname, base_hash in hashes.items():
            for compare_fname, compare_hash in hashes.items():
                if base_fname != compare_fname:
                    if np.count_nonzero(base_hash.hash != compare_hash.hash) <= diff_limit:
                        print("{} image found {}% similar to {}".format(compare_fname, similarity, base_fname))
                        # Add only unique images to the set for deletion
                        unique_similars.add(compare_fname)

        if unique_similars:
            print("\n{} Unique similar images found.".format(len(unique_similars)))
            a = input("Do you want to delete these unique images? Press Y or yN:  ").strip().lower()
            if a == "y":
                space_saved = 0
                for fname in unique_similars:
                    space_saved += os.path.getsize(fname)
                    os.remove(fname)
                    print("{} Deleted Successfully!".format(os.path.basename(fname)))
                print("\nYou saved approximately {} MB of space!".format(round(space_saved / 1_000_000, 2)))
            else:
                print("No images were deleted.")
        else:
            print("No Similar Images Found :(")
