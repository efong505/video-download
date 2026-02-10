# Git Commit Script
# Stages all changes, commits with message, and pushes to remote
# Usage: .\git-commit.ps1 "Your commit message"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

git add .
git commit -m $Message
git push