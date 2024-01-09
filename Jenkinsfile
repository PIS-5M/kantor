pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    image 'node:20.10.0-alpine3.19'
                }
            }
            steps {
                sh '''
              cd /var/jenkins_home/workspace/kantor5M_main/backend
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
            
            # Odczytaj obecną wersję z pliku pyproject.toml
            current_version = "1.0"
            
            # Inkrementuj pierwszą cyfrę i zresetuj drugą cyfrę do 0
            if [ "$1" == "nv" ]; then
                new_version=$(echo "$current_version" | awk -F'.' '{print $1 + 1 ".0"}')
            
            # Inkrementuj drugą cyfrę, jeśli parametr nv został podany
            else
                IFS='.' read -ra version_parts <<< "$current_version"
                new_second_digit=$((${version_parts[1]} + 1))
                new_version="${version_parts[0]}.$new_second_digit"
            fi
            
            # Aktualizuj plik pyproject.toml z nową wersją
            sed -i "s/version = \".*\"/version = \"$new_version\"/" pyproject.toml
            
            # Przejdź do katalogu i zbuduj paczkę pythonową
            cd "$(dirname "$0")" || exit
            python3 -m build
            
            echo "Pomyślnie utworzono paczkę pythonową dla nowego release'u backendu o numerze wersji: $new_version"
              
                ''' 
            }
        }
    }
}
