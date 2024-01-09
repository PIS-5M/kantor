pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        dockerfile true
      }
      steps {
        sh 'py.test /var/jenkins_home/workspace/kantor5M_main/backend/src/backend/test.py'
      }
    }

    stage('Build') {
      agent {
        docker {
          image 'python:3.12.1-alpine3.19'
        }

      }
      steps {
        ls pwd(tmp: true)
        sh 'cd var/jenkins_home/workspace/kantor5M_main@tmp/backend'
        sh './create_python_package'
      }
    }

  }
}
