

run:
	docker build -t genoss .
	docker run -it --rm -p 4321:4321 genoss