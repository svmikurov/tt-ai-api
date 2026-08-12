# Tech task CHCKZ project makefile

# Install dependencies
setup:
	poetry install

# Remove cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

# Build documentation (HTML)
docs-build:
	poetry run make -C docs html

# Clean documentation (HTML)
docs-clean:
	poetry run make -C docs clean

# Build docs and open in default browser
docs-open: docs-build
	xdg-open docs/build/html/index.html

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies"
	@echo "  make clean        - Remove cache files"
	@echo "  make docs-build   - Build HTML documentation"
	@echo "  make docs-clean   - Clean HTML documentation"
	@echo "  make docs-open    - Build docs and open in browser"
