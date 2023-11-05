## `arashnrim/arashnrim`'s update script

Welcome! If you're here, it means you're probably interested to know how the dynamic language count is done in the special profile README file. Thanks for stopping by!

This folder has everything for the script to work. The script is written in Python and is powered by a GitHub Actions workflow that is scheduled to run daily. If you're curious to check out the important files and what they're used for, here they are:

|                                              File                                               | Description                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|          [`main.py`](https://github.com/arashnrim/arashnrim/blob/main/update/main.py)           | The main script behind this project. This script is responsible for fetching languages of all my projects, then updating the README file in the folder outside of `update/`.                                           |
|           [`.cache`](https://github.com/arashnrim/arashnrim/blob/main/update/.cache)            | A text file that stores the language count during the last run, used in comparing languages between a previous and current run. If there are no changes, the script will not update the README file to save resources. |
|   [`.projectextras`](https://github.com/arashnrim/arashnrim/blob/main/update/.projectextras)    | A text file that stores projects not created by me but I still want to include in the language count. These are usually collaborative projects.                                                                        |
|   [`.projectignore`](https://github.com/arashnrim/arashnrim/blob/main/update/.projectignore)    | A text file that stores projects that I don't want to include in the language count. These are usually forked or negligible projects.                                                                                  |
| [`requirements.txt`](https://github.com/arashnrim/arashnrim/blob/main/update/requirements.txt)  | A standard file used by pip to install dependencies.                                                                                                                                                                   |
| [`update.yaml`](https://github.com/arashnrim/arashnrim/blob/main/.github/workflows/update.yaml) | The GitHub Actions workflow file that runs the script daily.                                                                                                                                                           |

## Walkthrough

Curious to know what the script does? Here's a quick rundown:

1. The script first writes a boilerplate to the README file, which includes headers and a self-introduction.
2. The script then tries to see if `.cache` exists, and if so, it reads the file and stores the language count in a variable.
3. The script then fetches all my repositories using the GitHub API, and stores the repository details in a variable.
4. If extra projects are mentioned in `.projectextras`, the script will fetch those repositories as well and add the details to the same variable.
5. A loop goes through each repository and begins tallying counts based on the language used in the repository.
6. If the cache data matches the current data, the script will not update the README file. Otherwise, it will update the README file with the new data.
7. The script writes the cache data to `.cache` for the next run.
8. The script writes the final part of the README file, which includes a footer and a timestamp.
9. The script writes the README file to the folder outside of `update/`.

The Actions workflow handles the rest, which includes installing dependencies, running the script, and committing the changes to the repository. Here's a quick rundown of what the workflow does:

1. At 12:00 a.m. UTC every day, the workflow will run.
2. The workflow will set up a Python version and install dependencies using `pip`.
3. The workflow loads in all the secrets needed to run the script, like the GitHub API token.
4. The workflow runs the script, letting it do its thing and update the README file.
5. The workflow uses Git to check if there are any changes to the repository.
6. If there are changes, the workflow will commit the changes and push them to the repository as the GitHub Actions bot.

If you want to learn more, here are some resources worth checking out:

- [GitHub Actions Documentation](https://docs.github.com/en/actions): The official documentation for GitHub Actions, perfect if you need to learn how to set up your own workflow.
- [Python Tutor](https://pythontutor.com/): A great tool to visualize how Python code works. It lets you step through the code line by line, and see how variables change as the code runs.

## Setting up

If you want to set up your own version of this script, here's what you need to do:

1. Create a personal access token. You can do this by going to your [GitHub settings](https://github.com/settings/tokens?type=beta).
   - You'll minimally need read-only access to contents, read-only access to metadata, and read and write access to workflows.
2. Fork this repository.
3. Go to your fork's settings, and open the Secrets and variables tab group. Open the Actions secrets tab.
4. Click the edit button for the `PAT` secret, and paste your personal access token in the box. Click the Update secret button.
5. That's it! The workflow will run daily, and you can check the Actions tab to see if it's working.

## License

This project is licensed under the [Unlicense](https://github.com/arashnrim/arashnrim/blob/main/LICENSE.md), meaning that you are allowed to do anything you want with the code. You can use it, modify it, sell it, and even claim it as your own if you want to. The only thing you can't do is hold me liable if something goes wrong. For more information, check out the license file.
