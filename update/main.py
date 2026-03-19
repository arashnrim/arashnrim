import json
from datetime import datetime
import logging
import sys
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logging.info(
    "Attempting to update languages in the root README.md file. Initiating...")

CONTENT = """
![A gallery of different pictures of people placed next to each other. In the foreground, a text that includes "Hey! I'm Arash. I'm driven to use tech in crafting intuitive, purposeful, and well-designed things that work for people."](docs/banner.webp)

## 👋 Hello world, I'm Arash!

This space is where I explore with code. I find joy in seeing the code I write come to life, whether it's a web project or a command-line interface. I like to think that [learning in public](https://garden.arash.codes/social/learning-in-public) is the best way I learn, so watch this space as I pick up (and occassionally break) things as I go!

---

### 🛠 What I've been using...

"""

cache = {}

try:
    open(".cache", encoding="utf-8")
except FileNotFoundError:
    logging.info("No cache found. Proceeding...")
else:
    logging.info("Found cache. Proceeding...")
    with open(".cache", encoding="utf-8") as file:
        languages = [language.strip().split(",")
                     for language in file.readlines()]
        for language in languages:
            cache[language[0]] = int(language[1])

logging.info("Attempting to reach GitHub's API...")
query = requests.get(
    "https://api.github.com/search/repositories?q=user:arashnrim", timeout=10, headers={
        "Authorization": f"token {os.getenv('PAT')}"
    })
count = {}

if query.status_code != 200:
    logging.critical(
        "Response from GitHub's API returned a non-OK (200) status code. Stopping process for safety.")
    sys.exit(-1)

query = json.loads(query.text)
logging.info("Retrieved details of repositories from GitHub's API.")

repos = [repo for repo in query["items"]]

# Reads in extra projects specified in `.projectextras`
logging.info("Attempting to read in extra projects...")
with open(".projectextras", encoding="utf-8") as file:
    read_count = 0
    for line in file.readlines():
        line = line.strip()

        # Check if the line matches the format `<owner>/<repo>` then extracts owner and repo if so
        if not re.match(r"^[-\w_.]+\/[-\w_.]+$", line):
            logging.warning(
                f"Invalid format for extra project: {line}. Skipping...")
            continue

        read_count += 1

        query = requests.get(
            f"https://api.github.com/repos/{line}", timeout=10, headers={
                "Authorization": f"token {os.getenv('PAT')}"
            })
        if query.status_code != 200:
            logging.warning(
                f"Response from GitHub's API returned a non-OK ({query.status_code}) status code for {line.strip()}. Skipping...")
            read_count -= 1
            continue

        repos.append(json.loads(query.text))

    logging.info(f"Read {read_count} extra project{
        "" if read_count == 1 else "s"}.")

# Reads in ignored projects specified in `.projectignore`
logging.info("Attempting to read in ignored projects...")
ignored = []
with open(".projectignore", encoding="utf-8") as file:
    read_count = 0
    for line in file.readlines():
        line = line.strip()

        read_count += 1

        # Check if the line matches the format `<owner>/<repo>`
        if not re.match(r"^[-\w_.]+\/[-\w_.]+$", line):
            logging.warning(
                f"Invalid format for ignored project: {line}. Skipping...")
            read_count -= 1
            continue

        ignored.append(line)

    logging.info(f"Read {read_count} ignored project{
        "" if read_count == 1 else 's'}.")

logging.info(f"Extracting languages from {
             len(repos)} repositories (including archived and {len(ignored)} ignored)...")
for repo in repos:
    if repo["archived"] or repo["full_name"] in ignored:
        continue
    if not repo["language"] is None:
        if repo["language"] in count:
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

CONTENT += "<table style=\"width: 100%\">\n"

space_tab = " " * 4
for language in count:
    CONTENT += f"{space_tab}<tr>\n"
    CONTENT += f"{space_tab *
                  2}<th scope=\"row\" style=\"text-align: right\">{language[0]}</th>\n"
    CONTENT += f"{space_tab * 2}<td>{language[1]} project{
        "" if language[1] == 1 else "s"}</td>\n"

    CONTENT += f"{space_tab}</tr>\n"

CONTENT += "</table>\n"

logging.info("Logging to cache...")
with open(".cache", "w", encoding="utf-8") as file:
    for language in count:
        file.write(f"{language[0]},{language[1]}\n")

logging.info("Appending end chunk...")
CONTENT += f"""
<sub>Last updated: {datetime.today().strftime("%d %B %Y")} — <a href="https://github.com/arashnrim/arashnrim/tree/main/update">curious about this?</a></sub>

---

If you're curious to learn more about me, feel free to [have a look at my website](https://arash.codes)! I know it can be daunting to say hi, but [if you do](https://arash.codes/#connect), I'll be sure to say hi. Feel free to also check out [`function()`](https://blog.arash.codes), my blog, and [Δ Delta](https://garden.arash.codes), my digital garden — I'm equally proud of both.

We're all learners in one way or another, and I hope your stop here has been helpful. Thank you for stopping by; go on and create awesome things!
"""

logging.info("Writing to file...")
with open("../README.md", "w", encoding="utf-8") as file:
    file.write(CONTENT)

logging.info("The program has completed successfully.")
