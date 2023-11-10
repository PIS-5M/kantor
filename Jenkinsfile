pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo '"Hello world!"'
        sh '''pip install pytest
'''
        sh 'pytest test_trial_file.py'
      }
    }

  }
}