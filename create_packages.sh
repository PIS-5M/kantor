#!/bin/bash

# Przyjmij parametr, jeśli został podany
if [ $# -eq 1 ]; then
    PARAMETER="$1"
else
    PARAMETER=""
fi

# Uruchom skrypt w podkatalogu ./backend
echo "Uruchamiam skrypt do tworzenia paczki backendu w podkatalogu./backend..."
(cd ./backend && chmod +x create_python_package.sh && ./create_python_package.sh "$PARAMETER")

# Uruchom skrypt w podkatalogu ./app
echo "Uruchamiam skrypt do tworzenia paczki frontendu w podkatalogu ./app..."
(cd ./app && chmod +x create_react_package.sh && ./create_react_package.sh "$PARAMETER")

echo "Operacja zakończona pomyślnie - paczki zostały utworzone."
