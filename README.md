# _sm-scraper_
Social Media Scraper (CMSC828D Final Project)

This final project idea is a collaboration with the Full Disclosure Project, through the National Association of Criminal Defense Lawyers. The goal is to develop a background process for continually scraping the web for relevant posts to social media sites, such as Twitter, Facebook, Instagram, Reddit, etc.. The targets of the scraping process are social media posts that mention potential misconduct by police officers in specific Jurisdictions. The deliverables for the project are: a) a public GitHub repository with clear and detailed instructions on how to setup and execute the scraper; b) a starting collection of social media posts produced by the scraper as an example dataset, with an explicit schema describing the structure of the scraped data; c) a separate script to extract relevant information uncovered by the scraper within each social media post; and d) ideally a prototype interface to visualize the extracted results.


### How to run _sm-scraper_
There are two ways to run this project, either within a Docker container or
directly on the local machine. After either setup, visit http://localhost/ in
your browser to see the dashboard.

1. **The Docker Way:**
    Simply run the commands in `run_sm-scraper_docker.sh` from the project's root
    directory.  
    You can do so either directly or using a unix shell:
    <pre>
    ./run_sm-scraper_docker.sh
    </pre>

2. **Without Docker:**
    To run the project without Docker you will need to have installed Python3
    (preferably Python 3.8) and PostgreSQL with a superuser 'cmsc828d' and a
    database 'smsdatabase'.  
    Then, run the commands in `run_sm-scraper_docker.sh` from the project's
    root directory.  
    You can do so either directly or using a unix shell like so:
    <pre>
    ./run_sm-scraper.sh
    </pre>
