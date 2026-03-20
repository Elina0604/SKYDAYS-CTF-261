FROM ubuntu:24.04 AS chroot

RUN userdel -r ubuntu && /usr/sbin/useradd --no-create-home -u 1000 user

COPY chal /home/user/chal
COPY flag.txt /home/user/
COPY secret /home/user/

# Make executable
RUN chmod +x /home/user/chal

FROM gcr.io/kctf-docker/challenge@sha256:413451e53e8ff4d359f551699e7b73594d0be5b87e7b2bd284bd3f9475418e7d

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
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/chal"
