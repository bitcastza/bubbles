COMPILER = pdflatex
UMLC = plantuml
BUILDDIR = build
DIAGRAMDIR = diagrams
SRC = $(wildcard *.tex)
DIAGRAM_SRC = $(wildcard $(DIAGRAMDIR)/*.txt)
TEX_OBJS = $(addprefix $(BUILDDIR)/, $(patsubst %.tex, %.pdf, $(SRC)))
DIAGRAM_OBJS = $(addprefix $(BUILDDIR)/, $(patsubst $(DIAGRAMDIR)/%.txt, %.png, $(DIAGRAM_SRC)))
TEX_OPT = -halt-on-error -output-directory $(BUILDDIR)
UML_OPT = -output ../$(BUILDDIR)

.PHONY: compile clean

compile: $(TEX_OBJS)

clean:
	rm -rf $(BUILDDIR)

$(BUILDDIR)/%.pdf: %.tex $(DIAGRAM_OBJS) | $(BUILDDIR)
	${COMPILER} ${TEX_OPT} $<
	${COMPILER} ${TEX_OPT} $<

$(DIAGRAM_OBJS): $(DIAGRAM_SRC) | $(BUILDDIR)
	$(UMLC) $(UML_OPT) $(DIAGRAM_SRC)

$(BUILDDIR):
	mkdir $(BUILDDIR)
