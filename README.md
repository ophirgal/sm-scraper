# sm-scraper
Social Media Scraper (CMSC828D Final Project)

This final project idea is a collaboration with the Full Disclosure Project, through the National Association of Criminal Defense Lawyers. The goal is to develop a background process for continually scraping the web for relevant posts to social media sites, such as Twitter, Facebook, Instagram, Reddit, etc.. The targets of the scraping process are social media posts that mention potential misconduct by police officers in specific Jurisdictions. The deliverables for the project are: a) a public GitHub repository with clear and detailed instructions on how to setup and execute the scraper; b) a starting collection of social media posts produced by the scraper as an example dataset, with an explicit schema describing the structure of the scraped data; c) a separate script to extract relevant information uncovered by the scraper within each social media post; and d) ideally a prototype interface to visualize the extracted results.


example:

    # Make sure to change `env/machie_config.bashrc` per machine
    make docker_build_example
    make example_shell
    /usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf &
    psql -h localhost -p 5432 -U cmsc828d -d a2database
