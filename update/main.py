import json
from datetime import datetime
import logging
import sys
import requests

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logging.info("Attempting to update languages in the root README.md file. Initiating...")

CONTENT = """
## 👋 Hello world, I'm Arash!

I'm a student with a passion for making a change through technology. While that one-liner is fairly ambiguous, it gives me a purpose and motivation to create interesting (and hopefully helpful!) stuff.

---

### 🛠 I'm using...

"""

cache = {}

try:
    open(".cache")
except FileNotFoundError:
    logging.info("No cache found. Proceeding...")
else:
    logging.info("Found cache. Proceeding...")
    with open(".cache") as file:
        languages = [language.strip().split(",") for language in file.readlines()]
        for language in languages:
            cache[language[0]] = int(language[1])

with open(".projectignore") as file:
    ignored_projects = file.readline().split(",")
logging.info("Read projects to ignore.")

logging.info("Attempting to reach GitHub's API...")
repos = requests.get("https://api.github.com/users/arashnrim/repos?sort=pushed")
languages = []
count = {}

if repos.status_code != 200:
    logging.critical("Response from GitHub's API returned a non-OK (200) status code. Stopping process for safety.")
    sys.exit(-1)

repos = json.loads(repos.text)
logging.info("Retrieved details of repositories from GitHub's API.")

logging.info("Extracting languages...")
for repo in repos:
    if repo["name"] in ignored_projects:
        continue
    if not repo["language"] is None:
        if repo["language"] in languages:
            count[repo["language"]] += 1
            continue
        else:
            count[repo["language"]] = 1
            languages.append(repo["language"])

if cache == count:
    logging.info("No change was found. Aborting process.")
    logging.info("The program has completed successfully.")
    sys.exit(0)

logging.info("Appending languages...")
for language in languages:
    CONTENT += "- {} (in {} project{})\n".format(language, count[language], "s" if count[language] != 1 else "")

logging.info("Logging to cache...")
with open(".cache", "w") as file:
    for key, value in count.items():
        file.write("{},{}\n".format(key, value))

logging.info("Appending end chunk...")
CONTENT += """
<sub>Last updated: {}</sub>

---

Feel free to <a href="mailto:hello@arashnrim.me" target="_blank" rel="noreferrer">be in contact</a> — after all, everyone's learning together! Thanks for stopping by, and go create awesome things!
""".format(datetime.today().strftime("%d %B %Y"))

logging.info("Writing to file...")
with open("../README.md", "w") as file:
    file.write(CONTENT)

logging.info("The program has completed successfully.")
