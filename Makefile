

include ./env/project_config.bashrc
include ./env/machine_config.bashrc



.PHONY: example_shell
.SILENT: example_shell
example_shell:
	xhost +local:docker \
	&& sudo docker run \
		--rm \
		--ipc=host \
		--net=host \
		-w '${PROJECT_DN}' \
		-v '/dev/shm:/dev/shm' \
		-v '${PROJECT_DN}:${PROJECT_DN}' \
		-v '${PROJECT_DN}/env/home/shu/.bashrc:/var/lib/postgresql/.bashrc' \
		-it '${PROJECT_NAME}:example' \
		bash
.PHONY: docker_build_example
docker_build_example:
	sudo docker build -t ${PROJECT_NAME}:example -f ./env/example.Dockerfile ./env
# make docker_build_example
# make example_shell
# /usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf &
# psql -h localhost -p 5432 -U cmsc828d -d a2database



.PHONY: nlp_jupyterlab
.SILENT: nlp_jupyterlab
nlp_jupyterlab:
	xhost +local:docker \
	&& sudo docker run \
		--rm \
		--ipc=host \
		--net=host \
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
.PHONY: docker_build_nlp
docker_build_nlp:
	sudo docker build -t ${PROJECT_NAME}:nlp -f ./env/nlp.Dockerfile ./env



.PHONY: docker_stop
docker_stop:
	sudo docker stop $(sudo docker ps -aq) && sudo docker rm $(sudo docker ps -aq)

.PHONY: docker_clean_dangling
docker_clean_dangling:
	sudo docker rmi $(sudo docker images --quiet --filter "dangling=true")


