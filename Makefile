all: cov

test: lint
	hatch run test

cov: lint
	hatch run cov

lint:
	hatch run types:check
	hatch fmt
