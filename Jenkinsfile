pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo '"Hello world!"'
        sh 'sh \'pytest test_trial_file.py\''
      }
    }

  }
}