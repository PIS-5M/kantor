pipeline {
  agent any
  stages {
    stage('Build') { 
            agent {
                dockerContainer {
                    image 'python:3.12.1-alpine3.19'
                }
              dockerContainer {
                image 'node:20.10.0-alpine3.19'
            }
            }
            steps {
                sh 'npm install'
                sh './create_packages.sh' 
            }
        }
    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}
