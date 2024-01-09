pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'sh \'python3 print("Hello world")\''
      }
    }

    stage('Test') {
      steps {
        echo '"Hello world!"'
      }
    }

  }
}