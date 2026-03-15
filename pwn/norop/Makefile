CC=gcc
CXX=g++

CFLAGS=-O2 -fstack-protector-strong
LDFLAGS=-Wall -Wextra

all: vuln tracer

vuln: vuln.c
	$(CC) vuln.c -o vuln $(CFLAGS) $(LDFLAGS)
	patchelf --set-interpreter ./libc/ld-linux-x86-64.so.2 ./vuln
	patchelf --replace-needed libc.so.6 ./libc/libc.so.6 ./vuln

tracer: tracer.cpp
	$(CXX) tracer.cpp -o tracer -lcapstone $(CFLAGS) $(LDFLAGS)

clean:
	rm -f vuln tracer
