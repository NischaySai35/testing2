# Bean & Brew — the broken version (testing2)

The same cafe website as `testing1`, but with **deliberate problems** so SecurePipe has something to catch:

- hardcoded password, API key, database URL and secret key in `app.py`
- a committed `.env` file (no `.gitignore`)
- SQL injection, `eval()`, a weak MD5 hash, a shell command built from user input, TLS checks off, unsafe YAML, debug mode
- old, vulnerable libraries (PyYAML 5.3.1, urllib3 1.25.8), an unpinned `requests`, conflicting PyYAML pins
- a Dockerfile that runs as root and copies `.env` into the image; a compose file with `privileged: true` and the Docker socket
- a Python file and a Java file with syntax errors

SecurePipe should **BLOCK** this repository.
