#!/usr/bin/env bash
# upgrade.sh — release a PySPARQL Anything version coupled to a SPARQL Anything release.
#
# Usage: ./upgrade.sh <sparql-anything-tag> [build-number] [options]
#   ./upgrade.sh v1.3.0-RC3            -> PyPI 1.3.0.0rc3 (pre-release)
#   ./upgrade.sh v1.3.0 1              -> PyPI 1.3.0.1
# Options:
#   --dry-run      prepare, test and build only; no commit/tag/push/upload/release
#   --skip-tests   don't run the test suite
#   --yes          don't ask for confirmation before publishing
#   --testpypi     upload to TestPyPI instead of PyPI (no GitHub release)
# Env:
#   PYTHON         interpreter for the test venv (default: python3; needs a pyjnius wheel, i.e. <= 3.14)
#   BRANCH_PREFIX  release branch prefix (default: release/)

set -euo pipefail

die()  { echo "ERROR: $*" >&2; exit 1; }
info() { echo "==> $*"; }

# ---- arguments --------------------------------------------------------------
SA_TAG="" BUILD="0" DRY_RUN=0 SKIP_TESTS=0 YES=0 TESTPYPI=0
for a in "$@"; do
  case "$a" in
    --dry-run)    DRY_RUN=1 ;;
    --skip-tests) SKIP_TESTS=1 ;;
    --yes)        YES=1 ;;
    --testpypi)   TESTPYPI=1 ;;
    -h|--help)    sed -n '2,17p' "$0"; exit 0 ;;
    -*)           die "unknown option $a" ;;
    *) if [[ -z "$SA_TAG" ]]; then SA_TAG="$a"; else BUILD="$a"; fi ;;
  esac
done
[[ -n "$SA_TAG" ]] || die "missing SPARQL Anything version (e.g. v1.3.0-RC3)"
[[ "$SA_TAG" == v* ]] || SA_TAG="v$SA_TAG"
[[ "$BUILD" =~ ^[0-9]+$ ]] || die "build number must be an integer"

# ---- version mapping: v1.3.0-RC3 -> 1.3.0.<build>rc3 ------------------------
re='^v([0-9]+\.[0-9]+\.[0-9]+)(-([A-Za-z]+)\.?([0-9]+))?$'
[[ "$SA_TAG" =~ $re ]] || die "unsupported tag format: $SA_TAG (expected vX.Y.Z or vX.Y.Z-RCn)"
BASE="${BASH_REMATCH[1]}"; KIND="$(tr '[:upper:]' '[:lower:]' <<<"${BASH_REMATCH[3]:-}")"; NUM="${BASH_REMATCH[4]:-}"
case "$KIND" in
  "")          SUFFIX="" ;;
  rc)          SUFFIX="rc$NUM" ;;
  alpha|a)     SUFFIX="a$NUM" ;;
  beta|b)      SUFFIX="b$NUM" ;;
  dev)         SUFFIX=".dev$NUM" ;;
  *)           die "unknown pre-release kind '$KIND' in $SA_TAG" ;;
esac
PY_VERSION="${BASE}.${BUILD}${SUFFIX}"
GIT_TAG="v${PY_VERSION}"
PRERELEASE=0; [[ -n "$SUFFIX" ]] && PRERELEASE=1
BRANCH="${BRANCH_PREFIX:-release/}${PY_VERSION}"
ABOUT="src/pysparql_anything/__about__.py"
JAR_URL="https://github.com/SPARQL-Anything/sparql.anything/releases/download/${SA_TAG}/sparql-anything-${SA_TAG}.jar"
PYTHON="${PYTHON:-python3}"
REPO_URL="pypi"; PYPI_JSON="https://pypi.org/pypi/pysparql-anything/${PY_VERSION}/json"
if (( TESTPYPI )); then REPO_URL="testpypi"; PYPI_JSON="https://test.pypi.org/pypi/pysparql-anything/${PY_VERSION}/json"; fi

info "SPARQL Anything ${SA_TAG} -> PySPARQL Anything ${PY_VERSION} (tag ${GIT_TAG}, pre-release: $([[ $PRERELEASE == 1 ]] && echo yes || echo no))"

# ---- preflight --------------------------------------------------------------
[[ -f "$ABOUT" && -f pyproject.toml ]] || die "run from the PySPARQL-Anything repo root"
for t in git curl "$PYTHON" java; do command -v "$t" >/dev/null || die "'$t' not found"; done
if (( ! DRY_RUN )); then
  (( TESTPYPI )) || { command -v gh >/dev/null || die "'gh' not found"; gh auth status >/dev/null 2>&1 || die "gh not authenticated (gh auth login)"; }
fi
for t in hatch twine; do command -v "$t" >/dev/null || die "'$t' not found (pip install $t)"; done
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || die "uncommitted changes to tracked files"
git fetch --tags origin
git rev-parse -q --verify "refs/tags/${GIT_TAG}" >/dev/null && die "tag ${GIT_TAG} already exists"
git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1 && die "remote branch ${BRANCH} already exists"
curl -fsIL -o /dev/null "$JAR_URL" || die "jar not found upstream: $JAR_URL"
[[ "$(curl -s -o /dev/null -w '%{http_code}' "$PYPI_JSON")" == 200 ]] && die "${PY_VERSION} already on ${REPO_URL}"

# ---- update version ---------------------------------------------------------
git checkout -b "$BRANCH"
"$PYTHON" - "$ABOUT" "$PY_VERSION" "$SA_TAG" <<'EOF'
import re, sys
path, ver, sa = sys.argv[1:]
src = open(path).read()
src, n1 = re.subn(r'^__version__ = ".*"$', f'__version__ = "{ver}"', src, flags=re.M)
src, n2 = re.subn(r'^__SparqlAnything__ = ".*"$', f'__SparqlAnything__ = "{sa}"', src, flags=re.M)
assert n1 == n2 == 1, "could not find version variables"
open(path, "w").write(src)
EOF
git diff --stat
rm -f src/pysparql_anything/*.jar   # has_jar() accepts any jar, so a stale one would mask the new version

# ---- test -------------------------------------------------------------------
if (( ! SKIP_TESTS )); then
  VENV="$(mktemp -d)/venv"
  info "testing in $VENV"
  "$PYTHON" -m venv "$VENV"
  "$VENV/bin/pip" install -q -e .
  ( cd tests && "$VENV/bin/python" test_library.py && "$VENV/bin/python" test_handler.py ) \
    || die "tests failed (branch ${BRANCH} left in place; jar under src/ may need removing)"
  rm -f src/pysparql_anything/*.jar
fi

# ---- build ------------------------------------------------------------------
rm -rf dist
hatch build ./dist
twine check dist/*
ls dist

if (( DRY_RUN )); then
  info "dry run: stopping before commit. Undo with: git checkout -- ${ABOUT} && git checkout - && git branch -D ${BRANCH}"
  exit 0
fi

# ---- confirm & publish ------------------------------------------------------
if (( ! YES )); then
  read -r -p "Commit, tag ${GIT_TAG}, push and upload ${PY_VERSION} to ${REPO_URL}? [y/N] " ok
  [[ "$ok" == [yY] ]] || die "aborted (branch ${BRANCH} has uncommitted changes)"
fi

git commit -am "Target SPARQL Anything ${SA_TAG}"
git tag -a "$GIT_TAG" -m "PySPARQL Anything ${PY_VERSION} (SPARQL Anything ${SA_TAG})"
git push origin "$BRANCH" "$GIT_TAG"

twine upload -r "$REPO_URL" dist/*

if (( ! TESTPYPI )); then
  NOTES="Coupled to SPARQL Anything ${SA_TAG} query engine."
  (( PRERELEASE )) && NOTES+=$'\n\n'"Pre-release: install with \`pip install --pre pysparql-anything\` or \`pip install pysparql-anything==${PY_VERSION}\`."
  GH_ARGS=(--title "$GIT_TAG" --notes "$NOTES" --verify-tag)
  (( PRERELEASE )) && GH_ARGS+=(--prerelease) || GH_ARGS+=(--latest)
  gh release create "$GIT_TAG" "${GH_ARGS[@]}" dist/*
fi

info "done: ${PY_VERSION} published to ${REPO_URL}. Verify with: pip install $([[ $PRERELEASE == 1 ]] && echo --pre) pysparql-anything==${PY_VERSION}"
