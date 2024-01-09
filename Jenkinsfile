pipeline {
  agent any
  stages {
    stage('Build') { 
            steps {
                sh './backend/create_packages.sh' 
            }
        }
    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}
