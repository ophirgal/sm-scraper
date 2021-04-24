# _sm-scraper_
Social Media Scraper (CMSC828D Final Project)

This final project idea is a collaboration with the Full Disclosure Project, through the National Association of Criminal Defense Lawyers. The goal is to develop a background process for continually scraping the web for relevant posts to social media sites, such as Twitter, Facebook, Instagram, Reddit, etc.. The targets of the scraping process are social media posts that mention potential misconduct by police officers in specific Jurisdictions. The deliverables for the project are: a) a public GitHub repository with clear and detailed instructions on how to setup and execute the scraper; b) a starting collection of social media posts produced by the scraper as an example dataset, with an explicit schema describing the structure of the scraped data; c) a separate script to extract relevant information uncovered by the scraper within each social media post; and d) ideally a prototype interface to visualize the extracted results.



# Running Containers

- Available containers: `db`, `scraper`, `dashboard`, and `nlp`.
- Supported Operation Systems: `windows`, `mac`, and `linux`.
- Change `env/machine_config.bashrc` w/ PROJECT_DN; absolute path to `sm-scraper`.
- Review dependencies in `env/<desired container>.Dockerfile`, and change the CMD
  line to your main module; see `env/nlp.Dockerfile` if you need an example.
- To run the project, if you're using a non-linux machine first run `make add_smscraper_net_<your host OS>`, e.g.
  for mac run `make add_smscraper_net_mac`.
- Then, to run individual containers run `make <desired container>_<your host OS>`; this automatically builds and runs the container.
- Start up other envs as you depend; i.e. `scraper` and `dashboard` both depend on `nlp`.
- If you want a shell, run `make <desired container>_shell` (currently applicable only
  for Linux machines).
