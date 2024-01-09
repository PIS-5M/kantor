pipeline {
  agent any
  stages {
    stage('Build') { 
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    image 'node:20.10.0-alpine3.19'
                }
            }
            steps {
                sh './create_packages.sh' 
                stash(name: 'compiled-results', includes: 'sources/*.py*') 
            }
        }
    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}
