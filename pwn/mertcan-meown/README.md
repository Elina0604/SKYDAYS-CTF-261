to build and start the docker:
```
docker build -t pwn .

docker run --privileged -p 1337:1337 -it pwn
```

to access to the pwn game:

```
nc localhost 1337
```
