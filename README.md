# _sm-scraper_
Social Media Scraper (CMSC828D Final Project)

This final project idea is a collaboration with the Full Disclosure Project, through the National Association of Criminal Defense Lawyers. The goal is to develop a background process for continually scraping the web for relevant posts to social media sites, such as Twitter, Facebook, Instagram, Reddit, etc.. The targets of the scraping process are social media posts that mention potential misconduct by police officers in specific Jurisdictions. The deliverables for the project are: a) a public GitHub repository with clear and detailed instructions on how to setup and execute the scraper; b) a starting collection of social media posts produced by the scraper as an example dataset, with an explicit schema describing the structure of the scraped data; c) a separate script to extract relevant information uncovered by the scraper within each social media post; and d) ideally a prototype interface to visualize the extracted results.



# running containers
- containers: db, scraper, dashboard, nlp
- change `env/machine_config.bashrc` w/ PROJECT_DN; absolute path to sm-scraper
- review dependencies in `env/{your_env}.Dockerfile`, and change CMD line to your main module; see `env/nlp.Dockerfile` if you need example
- to run, `make {your_env}`; this automatically builds the container too
- start up other envs as you depend; i.e. scraper depends on nlp
- if you want a shell, run `make {your_env}_shell`
