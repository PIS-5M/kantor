pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo '"Hello world!"'
        sh '''sh \'pip install pytest\'
sh \'pytest mytest.py\''''
      }
    }

  }
}