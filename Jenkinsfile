pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo '"Hello world!"'
        powershell 'pytest test_trial_file.py'
      }
    }

  }
}