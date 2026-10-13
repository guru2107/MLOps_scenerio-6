
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Docker Compose') {
            steps {
                bat 'docker --version'
                bat 'docker compose version'
                bat 'docker compose config -q'
            }
        }

        stage('Build Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker compose up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                powershell '''
                    $url = "http://localhost:5000"
                    $ready = $false

                    for ($i = 0; $i -lt 30; $i++) {
                        try {
                            $response = Invoke-WebRequest `
                                -Uri $url `
                                -TimeoutSec 3

                            if ($response.StatusCode -eq 200) {
                                $ready = $true
                                break
                            }
                        }
                        catch {
                            Start-Sleep -Seconds 2
                        }
                    }

                    if (-not $ready) {
                        docker compose ps
                        docker compose logs --tail 100
                        throw "Web application did not become ready."
                    }

                    Write-Output "Web application is responding."
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful. Application is deployed.'
            echo 'Open http://localhost:5000'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
