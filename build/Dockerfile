# MiKTeX environment for the full catalogue, including its Ubuntu x86_64 ZIP.
FROM ubuntu:24.04
COPY build/bootstrap-ubuntu.sh /tmp/bootstrap-ubuntu.sh
RUN sh /tmp/bootstrap-ubuntu.sh && rm -rf /var/lib/apt/lists/*
COPY build/python-requirement-lists /tmp/requirements
RUN python3 -m venv /opt/hku-venv && /opt/hku-venv/bin/python -m pip install --no-cache-dir \
    -r /tmp/requirements/general-pkgs.txt \
    -r /tmp/requirements/python-minted-pkgs.txt \
    -r /tmp/requirements/site-pkgs.txt

# A real user/home keeps on-demand package installation writable. Match the host
# UID at image build time so bind-mounted outputs belong to the invoking user.
ARG BUILD_UID=1000
RUN useradd --non-unique --uid "$BUILD_UID" --create-home --shell /bin/sh builder
COPY build/setup-miktex.sh /usr/local/bin/setup-miktex.sh
ENV PATH="/opt/hku-venv/bin:/home/builder/bin:${PATH}"
USER builder
RUN sh /usr/local/bin/setup-miktex.sh
WORKDIR /workspace
# Serialize cold builds that may install packages into the same MiKTeX tree.
CMD ["sh", "-c", "./configure && make site"]
