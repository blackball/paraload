.PHONY: clean c_idpool.so

c_idpool.so:
	gcc -shared -fPIC -o $@ idpool.c

clean:
	rm c_idpool.so
