TEXFILES := $(wildcard *.tex)
PDFFILES := $(TEXFILES:.tex=.pdf)
INTERMEDIATE := $(TEXFILES:.tex=.aux) $(TEXFILES:.tex=.log) $(TEXFILES:.tex=.out) $(TEXFILES:.tex=.toc)

all: $(PDFFILES)

%.pdf: %.tex
	latexmk -pdf $<

clean:
	rm -f $(PDFFILES) $(INTERMEDIATE)