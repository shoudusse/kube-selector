# kube-selector

Interactively switch between Kubernetes config files using a fuzzy finder.

## How it works

Scans `~/.kube/` for files matching `config-*`, presents them in an [fzf](https://github.com/junegunn/fzf) picker, and updates `~/.kube/config` (a symlink) to point to the selected file. The currently active config is shown at the top of the list.

## Requirements

- Python 3
- `fzf` installed and on your `PATH`
- Python dependency: `iterfzf`

```
pip install -r requirements.txt
```

## Setup

Name your kubeconfig files with a `config-` prefix inside `~/.kube/`:

```
~/.kube/
├── config          ← symlink managed by kube-selector
├── config-prod
├── config-staging
└── config-dev
```

## Usage

```
python kube-selector.py
```

Use arrow keys or type to filter, then press Enter to switch. Press Escape or Ctrl-C to cancel without making any changes.
