pipeline {
  agent any
  stages {
    stage('Build') { 
            agent {
              dockerContainer {
                image 'node:20.10.0-alpine3.19'
            }
            }
            steps {
                sh './app/create_react_package.sh' 
            }
        }
    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}
