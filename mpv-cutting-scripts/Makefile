INSTALLDIR:=/opt/mpv-cutting
#TMPDIR:=/tmp/tmp_mpv_$(PPID)
#TEST:=$(shell echo $(PPID) )

install: input.conf clip2.sh  encode2.sh  README.md  clip.sh   encode.sh   Makefile  set-var.sh
	echo Install is running ... cp to $(INSTALLDIR)
	cp input.conf $(HOME)/.mpv/
	ls -ltr ~/.mpv/
	sudo cp clip2.sh  encode2.sh  README.md  clip.sh   encode.sh   Makefile  set-var.sh $(INSTALLDIR)

	ls -ltr $(INSTALLDIR)

clip.mkv: $(INSTALLDIR)/clip.sh val-start val-end val-filename
	echo ... MAKEFILE ... creating clip.mkv ...... I am in directory 
	pwd
	sleep 1
	$(INSTALLDIR)/clip.sh

clip.webm: $(INSTALLDIR)/encode.sh clip.mkv val-filename val-humanstart
	echo ... MAKEFILE ... Now encoding is to come in directory
	pwd
	ls -lh *.mkv
	sleep 1
	$(INSTALLDIR)/encode.sh

clean:
	rm -rf *.mkv *.ass *.webm ~/.fonts/tmp val-end val-filename val-humanstart val-start *~

.PHONY: clean

