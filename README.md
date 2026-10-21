
# Password Security Checker
## Objective
A website that checks a password against common security vulnerabilities

## Planned security checks

- Common password check using a local password list
- Injection-safe input handling
- Compromised password check using the Have I Been Pwned Pwned Passwords API

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- The project files, including `Dockerfile` and `compose.yaml`

Python and Flask do not need to be installed separately.

## Run the website (Development)

1. Open **Docker Desktop** and make sure it is running.
2. Open the `password-checker` project folder in VS Code (or another terminal).
3. Open a terminal in the project folder.
4. Run:

   ```bash
   docker compose up
   ```

5. Open **http://127.0.0.1:5000** in your browser.

### Editing the website

Keep `docker compose up` running while editing.

- Changes to HTML, CSS, and JavaScript appear after refreshing the browser.
- Changes to Python files automatically reload the Flask development server.
- If you modify `Dockerfile` or `requirements.txt`, rebuild using:

  ```bash
  docker compose up --build
  ```

### Stop the website

Press **Ctrl+C** in the terminal running Docker Compose. To remove the stopped Compose containers, run:

```bash
docker compose down
```

## Run with Docker (Final Testing)

To run the application without Flask's development/debug server, from the project folder run:

```bash
docker build -t password-checker .
docker run --rm -p 127.0.0.1:5000:5000 password-checker
```

Open **http://127.0.0.1:5000**.

Press **Ctrl+C** to stop the container. The `--rm` option automatically removes the stopped container.
