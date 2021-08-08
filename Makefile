run:
	py -3 examples.py

install: glove.840B.300d.txt
	pip3 install --user numpy scipy

glove.840B.300d.txt:
	# Download from Stanford NLP GloVe page (Pennington et al.)
	wget https://nlp.stanford.edu/data/glove.840B.300d.zip && \
		unzip glove.840B.300d.zip

words.txt:
	# Requires unmunch from hunspell-tools and language files (.dic and .aff) from
	# https://cgit.freedesktop.org/libreoffice/dictionaries/tree/en
	for lang in AU CA GB US; do "C:\Users\chris\Downloads\hunspell-mingw-1.3.2-win32\hunspell-mingw-1.3.2-win32/bin/unmunch.exe" en_$$lang.dic en_$$lang.aff; done | \
		grep '^[a-z][a-z-]*[a-z]$$' | \
		sort -u > $@

.PHONY: run
.PHONY: install
