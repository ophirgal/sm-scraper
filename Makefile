

include ./env/project_config.bashrc
include ./env/machine_config.bashrc


############ SMSCRAPER NET #######
add_smscraper_net:
	sudo docker network create smscraper-net --subnet=172.28.0.0/16
add_smscraper_net_windows:
	docker network create smscraper-net --subnet=172.28.0.0/16

############ DATABASE ############

.PHONY: db_shell db db_docker
.SILENT: db_shell db
db_shell: db_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		--ip 172.28.0.9 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:db' \
		bash
db: db_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		--ip 172.28.0.9 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:db'
db_docker:
	sudo docker build -t ${PROJECT_NAME}:db -f ./env/db.Dockerfile ./env
db_windows: db_docker_windows
	docker run \
		--rm \
		--name db \
		--net smscraper-net \
		--ip 172.28.0.9 \
		-w '/workdir' \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:db'
db_docker_windows: 
	docker build -t ${PROJECT_NAME}:db -f ./env/db.Dockerfile ./env


############ SCRAPER ############

.PHONY: scraper_shell scraper scraper_docker
.SILENT: scraper_shell scraper
scraper_shell: scraper_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:scraper' \
		bash
scraper: scraper_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-t '${PROJECT_NAME}:scraper'
scraper_docker:
	sudo docker build -t ${PROJECT_NAME}:scraper -f ./env/scraper.Dockerfile ./env
scraper_windows: scraper_docker_windows
	docker run \
		--rm \
		--net smscraper-net \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-t '${PROJECT_NAME}:scraper'
scraper_docker_windows:
	docker build -t ${PROJECT_NAME}:scraper -f ./env/scraper.Dockerfile ./env


############ DASHBOARD ############

.PHONY: dashboard_shell dashboard dashboard_docker
.SILENT: dashboard_shell dashboard
dashboard_shell: dashboard_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		-p 5000:5000 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:dashboard' \
		bash
dashboard: dashboard_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net smscraper-net \
		-p 5000:5000 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:dashboard'
dashboard_docker:
	sudo docker build -t ${PROJECT_NAME}:dashboard -f ./env/dashboard.Dockerfile ./env
dashboard_windows: dashboard_docker_windows
	docker run \
		--rm \
		--name dashboard \
		--net smscraper-net \
		-p 5000:5000 \
		-w '/workdir' \
		-v '${PROJECT_DN}:/workdir' \
		-it '${PROJECT_NAME}:dashboard'
dashboard_docker_windows: 
	docker build -t ${PROJECT_NAME}:dashboard -f ./env/dashboard.Dockerfile ./env

############ NLP ############

.PHONY: nlp_jupyterlab nlp nlp_docker nlp_example
.SILENT: nlp_jupyterlab nlp nlp_example
nlp_jupyterlab: nlp_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--name nlp \
		--net smscraper-net \
		-p 9001:9001 \
		--ip 172.28.0.2 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-v '${PROJECT_DN}/env/project_config.bashrc:/root/project_config.bashrc' \
		-v '${PROJECT_DN}/env/machine_config.bashrc:/root/machine_config.bashrc' \
		-v '${PROJECT_DN}/env/home/shu/bin:/root/bin' \
		-v '${PROJECT_DN}/env/home/shu/.bashrc:/root/.bashrc' \
		-v '${PROJECT_DN}/env/home/shu/.jupyter:/root/.jupyter' \
		-v '${PROJECT_DN}/env/home/shu/.sensitive:/root/.sensitive' \
		-v '${PROJECT_DN}/env/home/shu/.cache/matplotlib:/root/.cache/matplotlib' \
		-v '${PROJECT_DN}/env/home/shu/.config/matplotlib:/root/.config/matplotlib' \
		-t '${PROJECT_NAME}:nlp' \
		jupyter lab \
			--notebook-dir / \
			--ip localhost --port 8888 \
			--allow-root --no-browser --ContentsManager.allow_hidden=True
nlp: nlp_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--name nlp \
		--net smscraper-net \
		-p 9001:9001 \
		--ip 172.28.0.2 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:nlp'
nlp_example: nlp_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--name nlp \
		--net smscraper-net \
		-p 9001:9001 \
		--ip 172.28.0.2 \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-it '${PROJECT_NAME}:nlp' \
		python3 -m src.nlp.example
nlp_docker:
	sudo docker build -t ${PROJECT_NAME}:nlp -f ./env/nlp.Dockerfile ./env
nlp_windows: nlp_docker_windows
	docker run \
		--rm \
		--ipc=host \
		--name nlp \
		--net smscraper-net \
		-p 9001:9001 \
		--ip 172.28.0.2 \
		-w '/workdir' \
		-v '${PROJECT_DN}:/workdir' \
		-it '${PROJECT_NAME}:nlp'
nlp_docker_windows:
	docker build -t ${PROJECT_NAME}:nlp -f ./env/nlp.Dockerfile ./env






############ EXAMPLE ############

.PHONY: example_shell example example_docker
.SILENT: example_shell example
example_shell: example_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net=host \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-v '${PROJECT_DN}/env/data/example/.bashrc:/var/lib/postgresql/.bashrc' \
		-it '${PROJECT_NAME}:example' \
		bash
example: example_docker
	sudo docker run \
		--rm \
		--ipc=host \
		--net=host \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-v '${PROJECT_DN}/env/data/example/.bashrc:/var/lib/postgresql/.bashrc' \
		-it '${PROJECT_NAME}:example'
example_docker:
	sudo docker build -t ${PROJECT_NAME}:example -f ./env/example.Dockerfile ./env
# make example
# psql -h localhost -p 5432 -U cmsc828d -d a2database


############ MISC ############

.PHONY: docker_stop
docker_stop:
	sudo docker stop $(sudo docker ps -aq) && sudo docker rm $(sudo docker ps -aq)

.PHONY: docker_clean_dangling
docker_clean_dangling:
	sudo docker rmi $(sudo docker images --quiet --filter "dangling=true")


