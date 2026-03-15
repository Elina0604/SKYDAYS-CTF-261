FROM ubuntu:24.04 as chroot

RUN userdel -r ubuntu && /usr/sbin/useradd --no-create-home -u 1000 user && apt update && apt install libcapstone4

COPY vuln /home/user/chal
COPY tracer /usr/local/bin/tracer
COPY flag.txt /home/user/
COPY ./libc/ld-linux-x86-64.so.2 /home/user/libc/
COPY ./libc/libc.so.6 /home/user/libc/

# Make executable
RUN chmod +x /home/user/chal

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

# --- FIX STARTS HERE ---
# Create the mount points inside the chroot so nsjail doesn't fail trying to create them as user 1000
RUN mkdir -p /chroot/dev && \
    touch /chroot/dev/null /chroot/dev/zero /chroot/dev/urandom && \
    chmod 666 /chroot/dev/null /chroot/dev/zero /chroot/dev/urandom
# --- FIX ENDS HERE ---

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /usr/local/bin/tracer /home/user/chal"
