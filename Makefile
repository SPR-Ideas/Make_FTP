install:
	pip3 install -r requirements.txt
	mkdir ~/.make_ftp
	cp make_ftp.py ~/.make_ftp/make_ftp
	echo "alias make-ftp='~/.make_ftp/make_ftp'" >> ~/.bashrc

test:
	pytest

clean:
	rm -r .pytest_cache
	rm -r __*

uninstall :
	rm -rf ~/.make_ftp
	sed -i "s#alias make-ftp='~/.make_ftp/make_ftp'##g" ~/.bashrc

