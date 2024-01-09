pipeline {
  agent any
  stages {
    stage('Build') { 
            steps {
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
