.PHONY: serve
all: public

public: content layouts projects static themes
	hugo

serve: content layouts projects static themes
	hugo serve -FD