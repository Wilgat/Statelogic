#!/bin/sh
set -eu

# =============================================
# statelogic build script — by Wong Chun Fai (wilgat)
# Pure POSIX sh, egg-info fully obliterated
# =============================================

PROJECT="statelogic"

# Get version from package (fallback to unknown)
VERSION=$(python3 -c "from src import statelogic; print(statelogic.__version__)" 2>/dev/null || \
          echo "unknown")

echo "statelogic build tool (v$VERSION)"
echo "========================================"

show_help() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  setup      Install/update build + twine
  clean      Remove ALL build artifacts, caches, and egg-info
  build      Build sdist + wheel
  upload     Upload to PyPI
  git        git add . -> commit -> push
  tag        Create and push git tag v$VERSION
  release    clean -> build -> upload -> tag (full release!)
  all        Same as release
  test       Run the test suite (pytest
             Optional arguments are passed directly to pytest.
             Examples:
               ./build.sh test
               ./build.sh test -k condense      # run only tests containing "condense"
               ./build.sh test test/testMatter.py::TestMatter::test_transition_gas_to_liquid_on_condense_when_temperature_is_low

Example:
  ./build.sh release
  ./build.sh test -v
EOF
}

do_setup() {
    echo "Installing/upgrading build tools..."
    pip3     install --upgrade build twine pytest
}

do_clean() {
    echo "Cleaning project (including all egg-info)..."
    rm -rf build dist .eggs .pytest_cache
    rm -rf statelogic.egg-info src/statelogic.egg-info src/statelogic.*.egg-info 2>/dev/null || true
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "._*" -delete 2>/dev/null || true
    echo "Clean complete — all egg-info destroyed"
}

do_build() {
    echo "Building package..."
    python3 -m build --sdist --wheel --outdir dist/
    echo "Build complete -> dist/"
    ls -lh dist/
}

do_upload() {
    echo "Uploading to PyPI..."
    twine upload dist/*
    echo ""
    echo "SUCCESS: $PROJECT v$VERSION is now live on PyPI!"
    echo "-> https://pypi.org/project/$PROJECT/$VERSION/"
}

do_git() {
    git add .
    echo "Enter commit message:"
    read -r message
    git commit -m "$message"
    git push
    echo "Pushed: $message"
}

do_tag() {
    if [ "$VERSION" = "unknown" ]; then
        echo "ERROR: Cannot determine version. Is __version__ set in src/statelogic/__init__.py?"
        exit 1
    fi

    TAG="v$VERSION"
    echo "Creating and pushing tag: $TAG"
    git tag -a "$TAG" -m "Release $TAG"
    git push origin "$TAG"
    echo "Tag $TAG created and pushed successfully!"
    echo "-> https://github.com/Wilgat/Statelogic/releases/tag/$TAG"
}

# NEW: run tests
do_test() {
    echo "Running test suite (pytest)..."
    # Ensure pytest is available
    if ! command -v pytest >/dev/null 2>&1; then
        echo "pytest not found – installing it temporarily..."
        python3 -m pip install --quiet pytest
    fi

    # If the package is already importable from src, add it to PYTHONPATH
    export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/src"

    # Run pytest on the test/ directory and pass through any extra args
    python3 -m pytest test/* "$@"
    echo "Tests finished."
}

# POSIX case
case "${1:-}" in
    setup)     do_setup     ;;
    clean)     do_clean     ;;
    build)     do_build     ;;
    upload)    do_upload    ;;
    git)       do_git       ;;
    tag)       do_tag       ;;
    test)      shift; do_test "$@" ;;           # <-- new command
    release|all)
               do_clean
               do_build
               do_upload
               do_tag
               ;;
    -h|--help|"") show_help ;;
    *)         echo "Unknown command: $1"; show_help; exit 1 ;;
esac

echo "Done."