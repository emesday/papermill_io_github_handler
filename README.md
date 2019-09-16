# Quick Start

```
$ pip install papermill
$ pip install git+https://github.com/mskimm/papermill_io_github_handler.git
$ export GITHUB_API_TOKEN=...
$ GIT_MESSAGE="some message" papermill \
    github+https://github.com/mskimm/papermill_io_github_handler/blob/master/tests/sample.ipynb \
    github+https://github.com/mskimm/papermill_io_github_handler/blob/master/tests/output.ipynb \
    -p msg 'hello world' \
    --no-request-save-on-cell-execute
   # without --no-request-save-on-cell-execute, the commits will be created each cell execution.
   # note that: --no-request-save-on-cell-execute fixed in #ref
```

# Environment Variables

```
GIT_NAME=<your name> # default: papermill
GIT_EMAIL=<your email> # default: (none)
GIT_MESSAGE=<some message> # default: updated by papermill
```

# Features

1. added scheme for GitHub as `github+https://`
   - `github+https://<github>/<user>/<repo>/blob/<ref_or_branch>/<path>`
2. read from/write to both GitHub and GitHub Enterprise
   - for example,
      - input: https://github.com/mskimm/papermill_io_github_handler/blob/master/tests/sample.ipynb
      - output: https://github.yourdomain.com/mskimm/notebooks/blob/master/sample-output.ipynb
         - `https://github.yourdomain.com` is the GitHub Enterprise URL
      ```
      $ export GITHUB_API_TOKEN=...
      $ export GITHUB_YOURDOMAIN_COM_API_TOKEN=...
      $ papermill \
          github+https://github.com/mskimm/papermill_io_github_handler/blob/master/tests/sample.ipynb \
          github+https://github.yourdomain.com/mskimm/notebooks/blob/master/sample-output.ipynb \
          -p msg 'hello world' \
          --no-request-save-on-cell-execute
      ```
