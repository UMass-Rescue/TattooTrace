from DuplicateRemover import DuplicateRemover

dirname = 'path/to/directory'  # Directory to search for duplicates
remover = DuplicateRemover(dirname)
remover.find_similar(similarity=90)