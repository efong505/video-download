param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

git add .
git commit -m $Message
git push