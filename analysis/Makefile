COMPILER = pdflatex
SRC = $(wildcard *.tex)
OBJ = $(patsubst %.tex, %.pdf, $(SRC))
TEX_OPT = -halt-on-error

compile: $(OBJ)

$(OBJ): $(SRC)
	${COMPILER} ${TEX_OPT} ${SRC}
	${COMPILER} ${TEX_OPT} ${SRC}

clean:
	rm -f *.pdf *.aux *.toc *.log
