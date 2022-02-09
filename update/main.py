import json
from datetime import datetime
import logging
import sys
import requests
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logging.info(
    "Attempting to update languages in the root README.md file. Initiating...")

CONTENT = """
## 👋 Hello world, I'm Arash!

I'm a student developer ardent about creating <dfn title="in a way that is aesthetically pleasing">designed</dfn>, <dfn title="in a way that feels natural to a user">intuitive</dfn>, and <dfn title="in a way that serves some use">practical</dfn> products using technology. I find that to be a rather ambitious statement, and rightfully so; I have a long way to go before getting there, but every step towards it counts!

I find joy in seeing the code I write come alive in one way or another — whether it's seeing it visually or just a command-line interface, most things I do are pretty interesting to me. I mostly deal with front-end web development at the moment, but would also like to have a go at any other parts of development.

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
        languages = [language.strip().split(",")
                     for language in file.readlines()]
        for language in languages:
            cache[language[0]] = int(language[1])

logging.info("Attempting to reach GitHub's API...")
query = requests.get(
    "https://api.github.com/search/repositories?q=user:arashnrim", headers={
        "Authorization": "token {}".format(os.getenv("PAT"))
    })
count = {}

if query.status_code != 200:
    logging.critical(
        "Response from GitHub's API returned a non-OK (200) status code. Stopping process for safety.")
    sys.exit(-1)

query = json.loads(query.text)
logging.info("Retrieved details of repositories from GitHub's API.")

repos = [repo for repo in query["items"]]

logging.info("Extracting languages...")
for repo in repos:
    if (repo["archived"] == True):
        continue
    if not repo["language"] is None:
        if repo["language"] in count.keys():
            count[repo["language"]] += 1
            continue
        else:
            count[repo["language"]] = 1

if cache == count:
    logging.info("No change was found. Aborting process.")
    logging.info("The program has completed successfully.")
    sys.exit(0)

logging.info("Sorting languages...")
count = sorted(count.items(), key=lambda language: language[1], reverse=True)

logging.info("Appending languages...")
for language in count:
    CONTENT += "- {} (in {} project{})\n".format(language[0],
                                                 language[1], "s" if language[1] != 1 else "")

logging.info("Logging to cache...")
with open(".cache", "w") as file:
    for language in count:
        file.write("{},{}\n".format(language[0], language[1]))

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
