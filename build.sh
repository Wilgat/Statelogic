#!/bin/sh
set -eu

# =============================================
# statelogic build script — by Wong Chun Fai (wilgat)
# Pure POSIX sh, egg-info fully obliterated
# Now works on Python2-only and Python3 systems automatically
# =============================================

PROJECT="statelogic"

# ——————————————————————————
# Simple Python 2/3 auto detection (pure POSIX, no bashisms)
# ——————————————————————————
if command -v python2 >/dev/null 2>&1 && python2 -c "import sys" 2>/dev/null; then
    PYTHON=python2
    if command -v pip2 >/dev/null 2>&1; then
        PIP=pip2
    else
        PIP="python2 -m pip"
    fi
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys" 2>/dev/null; then
    PYTHON=python3
    if command -v pip3 >/dev/null 2>&1; then
        PIP=pip3
    else
        PIP="python3 -m pip"
    fi
elif command -v python >/dev/null 2>&1 && python -c "import sys; sys.exit(0 if sys.version_info >= (3,) else 1)" 2>/dev/null; then
    PYTHON=python
    if command -v pip >/dev/null 2>&1; then
        PIP=pip
    else
        PIP="python -m pip"
    fi
else
    echo "ERROR: No working Python interpreter found (python2 or python3 required)"
    exit 1
fi

# Final fallback – if the chosen pip doesn't actually work, force module mode
if ! $PIP --version >/dev/null 2>&1; then
    PIP="$PYTHON -m pip"
fi

echo "Detected Python interpreter: $PYTHON"
echo "Using pip command         : $PIP"
echo

# Get version from package (fallback to unknown)
VERSION=$($PYTHON -c "from src import statelogic; print(statelogic.__version__)" 2>/dev/null || echo "unknown")

echo "statelogic build tool (v$VERSION)"
echo "========================================"

show_help() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  setup      Install/update build + twine + pytest
  clean      Remove ALL build artifacts, caches, and egg-info
  build      Build sdist + wheel
  upload     Upload to PyPI
  git        git add . -> commit -> push
  tag        Create and push git tag v$VERSION
  release    test       Run the test suite (pytest)
             Optional arguments are passed directly to pytest.
  release    clean -> build -> upload -> tag (full release!)
  all        Same as release

Example:
  ./build.sh release
  ./build.sh test -v
  ./build.sh test -k condense
EOF
}

do_setup() {
    echo "Installing/upgrading build tools..."
    $PIP install --upgrade build twine pytest
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
    $PYTHON -m build --sdist --wheel --outdir dist/
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

do_test() {
    echo "Running test suite (pytest)..."
    # Make sure pytest is there
    if ! command -v pytest >/dev/null 2>&1; then
        echo "pytest not found – installing it temporarily..."
        $PYTHON -m pip install --quiet pytest
    fi

    # Make the package importable from src/
    export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/src"

    # Run pytest and pass all extra args
    $PYTHON -m pytest test/* "$@"
    echo "Tests finished."
}

# ====================================
# Main command dispatcher
# ====================================
case "${1:-}" in
    setup)     do_setup     ;;
    clean)     do_clean     ;;
    build)     do_build     ;;
    upload)    do_upload    ;;
    git)       do_git       ;;
    tag)       do_tag       ;;
    test)      shift; do_test "$@" ;;
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