pipeline {
  agent any
  stages {
    stage('Build') { 
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
