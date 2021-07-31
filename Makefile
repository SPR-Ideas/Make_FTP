install:
	pip3 install -r requirements.txt
	mkdir ~/.make_ftp
	cp make_ftp.py ~/.make_ftp/make_ftp
	echo "alias make_ftp='~/.make_ftp/make_ftp'" >> ~/.bashrc

test:
	pytest


