#!/usr/bin/env groovy

podTemplate(label: 'mypod', containers: [
    containerTemplate(name: 'python', image: 'python:3.6', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true)
  ],
  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
  ]
  ) {
    node('mypod') {

        def myRepo = checkout scm
        def gitCommit = myRepo.GIT_COMMIT
        def gitBranch = myRepo.GIT_BRANCH
        def shortGitCommit = "${gitCommit[0..7]}"

        stage('Check running containers') {
            container('docker') {
                echo "${shortGitCommit}"
                sh "docker ps"
            }
        }

        stage('Python test') {
            container('python') {
                sh """
                    pip install -r requirements.txt
                    pytest -v
                   """
            }
        }

        stage('Python build') {
            container('python') {
                sh "pip install ."
            }
        }
    }
}
