pipeline {
  agent any
  stages {
    stage('Build') { 
            steps {
                sh './backend/create_python_package.sh' 
            }
        }
    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}
