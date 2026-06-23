from git import Repo
working_tree_dir = "/workspaces/disdrometer"
repo = Repo(working_tree_dir)
repo.git.add(A=True)
repo.git.commit('-m', 'updated data')
repo.git.push('origin', 'main')