
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Validate Docker Compose') {
            steps {
                bat 'docker --version'
                bat 'docker compose version'
                bat 'docker compose config -q'
                echo 'Docker Compose configuration is valid.'
            }
        }

        stage('Build Images') {
            steps {
                bat 'docker compose build'
                echo 'Docker images built successfully.'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker compose up -d'
                echo 'Application containers started.'
            }
        }

        stage('Smoke Test') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $baseUrl = "http://localhost:5000/"
                    $ready = $false

                    Write-Host "Waiting for the web application..."

                    for ($i = 1; $i -le 15; $i++) {
                        try {
                            $response = Invoke-WebRequest `
                                -Uri $baseUrl `
                                -UseBasicParsing `
                                -TimeoutSec 5

                            if ($response.StatusCode -eq 200) {
                                $ready = $true
                                Write-Host "Homepage returned HTTP 200."
                                break
                            }
                        }
                        catch {
                            Write-Host "Attempt $i failed: $($_.Exception.Message)"
                        }

                        Start-Sleep -Seconds 2
                    }

                    if (-not $ready) {
                        throw "Web application did not become ready."
                    }

                    Write-Host "Testing the ML prediction endpoint..."

                    $body = @{
                        sepal_length = "5.1"
                        sepal_width  = "3.5"
                        petal_length = "1.4"
                        petal_width  = "0.2"
                    }

                    $prediction = Invoke-WebRequest `
                        -Uri "http://localhost:5000/predict" `
                        -Method POST `
                        -Body $body `
                        -ContentType "application/x-www-form-urlencoded" `
                        -UseBasicParsing `
                        -TimeoutSec 10

                    if ($prediction.StatusCode -ne 200) {
                        throw "Prediction endpoint returned HTTP $($prediction.StatusCode)."
                    }

                    if ($prediction.Content -notmatch "Iris-setosa") {
                        throw "Prediction response did not contain the expected Iris-setosa result."
                    }

                    Write-Host "Prediction endpoint returned HTTP 200."
                    Write-Host "ML prediction smoke test passed."
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS: Build, deployment, and smoke tests completed.'
        }

        failure {
            echo 'Pipeline FAILED. Collecting container diagnostics.'

            powershell '''
                Write-Host "=== Container Status ==="
                docker compose ps

                Write-Host "=== Recent Container Logs ==="
                docker compose logs --tail 50
            '''
        }

        always {
            echo 'CI/CD pipeline execution completed.'
        }
    }
}
