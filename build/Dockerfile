# Optional environment for building the complete catalogue, including its Ubuntu ZIP.
FROM ubuntu:24.04
COPY build/bootstrap-ubuntu.sh /tmp/bootstrap-ubuntu.sh
RUN sh /tmp/bootstrap-ubuntu.sh && rm -rf /var/lib/apt/lists/*
COPY build/python-requirement-lists /tmp/requirements
RUN python3 -m venv /opt/hku-venv && /opt/hku-venv/bin/python -m pip install --no-cache-dir \
    -r /tmp/requirements/general-pkgs.txt \
    -r /tmp/requirements/python-minted-pkgs.txt \
    -r /tmp/requirements/site-pkgs.txt
ENV PATH="/opt/hku-venv/bin:${PATH}"
ENV TEXMFVAR=/tmp/hku-texmf-var
WORKDIR /workspace
CMD ["sh", "-c", "./configure && make -j2 site"]
