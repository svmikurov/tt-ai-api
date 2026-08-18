# ---------- Setup ----------

setup:
	poetry install

# ---------- Documentation ----------

docs-build:
	poetry run make -C docs html

docs-clean:
	poetry run make -C docs clean

docs-rebuild: docs-clean docs-build

docs-open: docs-build
	xdg-open docs/build/html/index.html 2>/dev/null || true

# ---------- Check / Test ----------

type-check:
	poetry run mypy .

lint:
	poetry run ruff check

fix:
	poetry run ruff check --fix

format:
	poetry run ruff format

test:
	poetry run pytest

check: format fix type-check test

# ---------- Docker ----------

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docs-docker-run:
	docker build -t docs -f docker/docs/Dockerfile .
	docker run -d -p 8000:8000 --name docs docs
	sleep 2
	xdg-open http://localhost:8000 2>/dev/null || true

docs-docker-stop:
	docker stop docs 2>/dev/null || true
	docker rm docs 2>/dev/null || true
	
# ---------- Clean ----------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# ---------- Help ----------

help:
	@echo "==================="
	@echo "Available commands:"
	@echo "==================="
	@echo ""
	@echo "Setup commands:"
	@echo "  make setup        	- Install dependencies"
	@echo "  make clean        	- Remove cache files"
	@echo ""
	@echo "Documentation commands:"
	@echo "  make docs-build   	- Build HTML documentation"
	@echo "  make docs-clean   	- Clean HTML documentation"
	@echo "  make docs-rebuild  - Rebuild HTML documentation"
	@echo "  make docs-open    	- Build and open docs in browser"
	@echo "  make docs-docker-run	- Build & run docs in Docker, open in browser"
	@echo "  make docs-docker-stop	- Stop docs Docker container
	@echo ""
	@echo "Server commands:"
	@echo "  make server-run   	- Run API server (port 8000)"
	@echo "  make server-kill	- Stop API server"
	@echo "  make server-restart	- Restart API server"
	@echo ""
	@echo "Check"
	@echo "  lint			- Lint code (read-only, no fixes)"
	@echo "  fix			- Auto-fix lint issues"
	@echo "  format		- Format code"
	@echo "  check			- Full pre-commit check (format + fix + type-check + test)"
	@echo "  type-check		- Check types (mypy)"
	@echo "  test			- Run pytest"
	@echo ""
	@echo "Other:"
	@echo "  make help		- Show this help"
	@echo ""
	@echo "📌 Note: Local commands (setup, docs-build, server-run, etc.)"
	@echo "   require Python virtual environment activated."
	@echo "   Docker commands work on Linux, macOS, and Windows."