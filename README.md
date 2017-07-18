# dinar-trader
Trade Dinars

## Clone repo
`git clone https://github.com/adamhyman/dinar-trader`

## Installation
Install the support libraries using the following pip command:
`pip install requests websocket-client bintrees gdax krakenex`

## Misc Git Commands
### Switch branch
`git checkout develop`

### Update Submodules
`git submodule update --init --recursive`

### Running the code
Run exchange_query.py in the root directory of this repository

### Add files
`git add <filename>`

Note: files should be added one at a time

### Commit
`git commit`

Note: the `-a` operator "shotguns" all your files into the commit. You rarely want to do this.

### Push all changes
`git push origin develp -m "comment"`

## Drop all changes and download everything from repo again
git reset --hard; git pull

Note: this will erase ALL changed files
