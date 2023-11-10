pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo '"Hello world!"'
        powershell 'python3 trial_file.py'
      }
    }

  }
}