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
              #!/bin/bash

# Przyjmij parametr, jeśli został podany
if [ $# -eq 1 ]; then
    PARAMETER="$1"
else
    PARAMETER=""
fi

# Uruchom skrypt w podkatalogu ./backend
echo "Uruchamiam skrypt do tworzenia paczki backendu w podkatalogu./backend..."
(chmod +x /var/jenkins_home/workspace/kantor5M_main/backend/create_python_package.sh && ./var/jenkins_home/workspace/kantor5M_main/backend/create_python_package.sh "$PARAMETER")

# Uruchom skrypt w podkatalogu ./app
echo "Uruchamiam skrypt do tworzenia paczki frontendu w podkatalogu ./app..."
(cd  && chmod +x create_react_package.sh && ./create_react_package.sh "$PARAMETER")

echo "Operacja zakończona pomyślnie - paczki zostały utworzone."
                ''' 
            }
        }
    }
}
