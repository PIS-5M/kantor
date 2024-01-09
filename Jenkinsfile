pipeline {
    agent none 
    stages {
        stage('Test') { 
            agent {
                docker {
                    dockerfile true
                }
            }
            steps {
                sh 'py.test /var/jenkins_home/workspace/kantor5M_main/test_trial_file.py'
            }
        }
    }
}
