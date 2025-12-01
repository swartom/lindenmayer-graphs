##
# Lindenmayer Graphs Reproducability Repository
#
# @file
# @version 0.1

PHONY: all

mkdir:
	mkdir -p figs

hypercube:
	python hyper_cube

all: mkdir hypercube

# end
