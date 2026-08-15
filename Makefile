# ============================================
# Tech task CHCKZ project makefile
# ============================================

.PHONY: setup clean docs-build docs-clean docs-open server-run server-kill help

# ---------- Setup ----------
setup:
	poetry install

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true


# ---------- Documentation ----------
docs-build:
	poetry run make -C docs html

docs-clean:
	poetry run make -C docs clean

docs-open: docs-build
	xdg-open docs/build/html/index.html


# ---------- Server ----------
server-run:
	poetry run uvicorn src.sd.entrypoint.main:app --reload --host 0.0.0.0 --port 8000

server-kill:
	-pkill -f "uvicorn src.sd.entrypoint.main:app" || true

server-restart: server-kill server-run


# ---------- Check / Test ----------

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-check:
	./check.sh

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
	@echo "  make docs-open    	- Build and open docs in browser"
	@echo ""
	@echo "Server commands:"
	@echo "  make server-run   	- Run API server (port 8000)"
	@echo "  make server-kill	- Stop API server"
	@echo "  make server-restart	- Restart API server"
	@echo ""
	@echo "Other:"
	@echo "  make help		- Show this help"