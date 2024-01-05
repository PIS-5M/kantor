#!/bin/bash

show_help() {
    echo "Usage: $0 [nv]"
    echo "  nv: Increments the first digit of the version and reset the second digit to 0. Used to release major update - a new version of the project."
    echo "  Without nv: Increments the second digit of the version. Used to release smaller updates of the project."
    exit 0
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    show_help
fi

# Odczytaj obecną wersję z pliku package.json
current_version=$(jq -r .version package.json)

# Inkrementuj pierwszą cyfrę i zresetuj drugą cyfrę do 0
if [ "$1" == "nv" ]; then
    new_version=$(echo "$current_version" | awk -F'.' '{print $1 + 1 ".0"}')

# Inkrementuj drugą cyfrę, jeśli parametr nv został podany
else
    IFS='.' read -ra version_parts <<< "$current_version"
    new_second_digit=$((${version_parts[1]} + 1))
    new_version="${version_parts[0]}.$new_second_digit"
fi

# Aktualizuj plik package.json z nową wersją
jq --arg new_version "$new_version" '.version = $new_version' package.json > tmp_package.json
mv tmp_package.json package.json

# Zainstaluj zależności i przygotuj produkcyjną wersję paczki
npm install
npm pack

echo "Pomyślnie utworzono paczkę reactową dla nowego release'u frontendu o numerze wersji: $new_version"
