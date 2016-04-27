TITLE=mouse

all:
	pdflatex $(TITLE).tex
	bibtex $(TITLE)
	pdflatex $(TITLE).tex
	pdflatex $(TITLE).tex

participate.pdf: participate.tex
	pdflatex participate.tex

clean:
	rm *.{aux,log,out,blg,bbl}
