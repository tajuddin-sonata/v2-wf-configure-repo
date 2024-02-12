def artifact_version

pipeline {
    agent {
        label 'jenkins-slave'
    }

    parameters{
        choice(name: 'ENVIRONMENT', choices:[
            'dev',
            'stg',
            'prod'],
            description: 'Choose which environment to deploy to.')
        
        string(name: 'VERSION', description: 'Explicit version to deploy (i.e., "v0.1"). Leave blank to build latest commit')
        
        
        string(name: 'AZURE_FUNCTION_NAME', defaultValue:'dev-wf-configure', description: '''The name of FunctionApp to deploy
            dev-wf-configure 
            stg-wf-configure
            prod-wf-configure''' )

        string(name: 'AZURE_FUNCTION_ASP_NAME', defaultValue:'', description: '''The name of App service Plan for FunctionApp to deploy
            v2-functions-ASP
            jenkins-ASP
            dev-wf-configure-ASP 
            stg-wf-configure-ASP
            prod-wf-configure-ASP''' )
        
        
        string(name: 'FUNC_STORAGE_ACCOUNT_NAME', defaultValue:'', description: '''select the existing Storage account name for Func App or create new .
            v2funcappstg569650
            ccadevfunctionappstgacc 
            ''' )

        string(name: 'AZURE_APP_INSIGHTS_NAME', defaultValue:'', description: '''The name of Existing Application insight for FunctionApp.
            v2-func-app-insight
            ''' )
        
        // string(name: 'APP_INSIGHTS_INSTRUMENTATION_KEY', description: '''select the existing Application insight Instrumentation Key .
        //     9b3a9c7a-fec6-4f67-b669-a149294fbeee 
        //     ''' )

        string(name: 'REGION', defaultValue:'Central India',  description: '''Region to Deploy to.
        East US, East US 2, West US, West US 2, 
        Australia East, Australia Southeast, Australia Central, Australia Central 2, Southeast Asia 
        South India, Central India, West India''')

        // choice(name: 'SUBSCRIPTION', choices:[
        //     '48986b2e-5349-4fab-a6e8-d5f02072a4b8',
        //     '34b1c36e-d8e8-4bd5-a6f3-2f92a1c0626e',
        //     '70c3af66-8434-419b-b808-0b3c0c4b1a04'
        //     ],
        //     description: 'Subscription to deploy to .')

        string(name: 'SUBSCRIPTION', defaultValue:'', description: ''' select subscription as:
            48986b2e-5349-4fab-a6e8-d5f02072a4b8
            34b1c36e-d8e8-4bd5-a6f3-2f92a1c0626e
            70c3af66-8434-419b-b808-0b3c0c4b1a04''')

        string(name: 'RESOURCE_GROUP_NAME', defaultValue:'', description: ''' Azure Resource Group in which the FunctionApp need to deploy.
            jenkins-247-rg
            ''')
        
        string(name: 'PRIVATE_ENDPOINT_NAME', defaultValue:'', description: ''' Private endpoint name.
            jenkins-private-endpoint
            ''')

        string(name: 'PRIVATE_CONNECTION_NAME', defaultValue:'', description: ''' Private endpoint Connection name.
            jenkins-privateend-connection
            ''')

        string(name: 'VNET_NAME', defaultValue:'', description: ''' Vnet name for Private endpoint connection & Vnet integration.
            jenkins-vm-vnet
            ''')

        string(name: 'INBOUND_SNET_NAME', defaultValue:'', description: ''' Inbound Subnet name for Private endpoint connection.
            jenkins-subnet
            ''')

        // string(name: 'OUTBOUND_VNET_NAME', description: ''' Outbound Vnet name for Vnet integration.
        //     jenkins-vm-vnet
        //     ''')

        string(name: 'OUTBOUND_SNET_NAME', defaultValue:'', description: ''' Outbound Subnet name for Private endpoint connection.
            jenkins-subnet-01
            ''')

        // choice(name: 'RESOURCE_GROUP_NAME', choices:[
        //     'jenkins-247-rg',
        //     'jenkins-247-rg'
        //     ],
        //     description: 'Azure Resource Group in which the FunctionApp need to deploy.')

        choice(name: 'SKU', choices:[
            'S3','S1', 'S2',
            'B1', 'B2', 'B3', 
            'P1V3','P2V3', 'P3V3'], 
            description: 'ASP SKU.')

        choice(name: 'PYTHON_RUNTIME_VERSION', choices:[
            '3.9',
            '3.10',
            '3.11'],
            description: 'Python runtime version.')
    }

    environment {
        AZURE_CLIENT_ID = credentials('azurerm_client_id')
        AZURE_CLIENT_SECRET = credentials('azurerm_client_secret')
        AZURE_TENANT_ID = credentials('azurerm_tenant_id')
        ZIP_FILE_NAME = "${params.AZURE_FUNCTION_NAME}"
        SONARQUBE_SCANNER_HOME = tool 'sonarscanner-5'
        functionAppId="/subscriptions/${params.SUBSCRIPTION}/resourceGroups/${params.RESOURCE_GROUP_NAME}/providers/Microsoft.Web/sites/${params.AZURE_FUNCTION_NAME}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                // git branch: 'dev', url: 'https://github.com/tajuddin-sonata/v2-wf-configure-repo.git'
                
                // Install Pip
                // sh 'sudo yum install -y python3-pip'

                // Install project dependencies
                // sh 'pip3 install -r requirements.txt -t .'
            }
        }

        // stage('Package Code') {
        //     steps {
        //         sh "zip -r ${ZIP_FILE_NAME} ."
        //     }
        // }

        /*
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-9.9') {
                    script {
                        sh """
                            echo "SonarQube Analysis"
                            
                            ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                                -Dsonar.projectKey=My-Configure-Project \
                                -Dsonar.host.url=http://4.240.69.23:9000 \
                                -Dsonar.sources=src \
                                -Dsonar.sourceEncoding=UTF-8 \
                                -Dsonar.python.version=3.11
                        """
                    }
                }
            }
        }
        */

        stage('SonarQube Analysis') {
            steps {
                echo "SonarQube Analysis !!"
                withSonarQubeEnv('sonarqube-9.9') {
                    sh '/opt/sonarscanner/bin/sonar-scanner'
                }
            }
        }

        /*
        stage ('Quality Gate') {
            steps {
                script {
                    echo "Quality Gate Check"
                    timeout(time: 1, unit: 'HOURS') {
                        def qg = waitForQualityGate()
                        if (dq.status != 'OK') {
                            error "Pipeline aborted due to quality failure: ${qg.status}"
                            currentBuild.result = 'FAILURE'

                        }
                    }
                }
            }
        }
        */
        

        stage('Create FunctionApp') {
            steps {
                // Login to azure using service principal
                sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID'
                sh "az account set --subscription ${params.SUBSCRIPTION}"
                
                // Create ASP for functionApp
                sh "az appservice plan create --name ${params.AZURE_FUNCTION_ASP_NAME} --resource-group ${params.RESOURCE_GROUP_NAME} --sku ${params.SKU} --is-linux --location ${params.REGION}"
                
                // Create FunctionApp
                sh "az functionapp create --name ${params.AZURE_FUNCTION_NAME} --resource-group ${params.RESOURCE_GROUP_NAME} --plan ${params.AZURE_FUNCTION_ASP_NAME} --runtime python --runtime-version ${params.PYTHON_RUNTIME_VERSION} --functions-version 4 --storage-account ${params.FUNC_STORAGE_ACCOUNT_NAME} --app-insights ${params.AZURE_APP_INSIGHTS_NAME}"
                
                // Vnet Integration
                sh "az functionApp vnet-integration add -g ${params.RESOURCE_GROUP_NAME} -n ${params.AZURE_FUNCTION_NAME} --vnet ${params.VNET_NAME} --subnet ${params.OUTBOUND_SNET_NAME}"
                
                // Enabling Private end points
                sh "az network private-endpoint create -g ${params.RESOURCE_GROUP_NAME} -n ${params.PRIVATE_ENDPOINT_NAME} --vnet-name ${params.VNET_NAME} --subnet ${params.INBOUND_SNET_NAME} --private-connection-resource-id $functionAppId --connection-name ${params.PRIVATE_CONNECTION_NAME} -l '${params.REGION}' --group-id sites"
            }
        }

        stage('Deploy artifacts to Nexus & Azure') {
            steps {
                script {
                    echo "Deploy artifact to Nexus & Azure !!!"
                    def ver = params.VERSION
                    sh """
                        #!/bin/bash
                
                        if [ -z "$ver" ]; then
                            artifact_version=\$(git describe --tags)
                            echo "\${artifact_version}" > src/version.txt
                            cd src
                            zip -r "../$ZIP_FILE_NAME-\${artifact_version}.zip" *
                            cd $WORKSPACE
                            echo "CREATED [$ZIP_FILE_NAME-\${artifact_version}.zip]"
                            curl -v -u admin:admin@123 --upload-file \
                                "$ZIP_FILE_NAME-\${artifact_version}.zip" \
                                "http://20.40.49.121:8081/repository/ci-config-service/$ZIP_FILE_NAME-\${artifact_version}.zip"
                        else
                            artifact_version=$ver
                            echo "Downloading specified artifact version from Nexus..."
                            curl -v -u admin:admin@123 -O "http://20.40.49.121:8081/repository/ci-config-service/ZIP_FILE_NAME-\${artifact_version}.zip"
                        fi
                        rm -rf "$ZIP_FILE_NAME-\${artifact_version}"
                        unzip "$ZIP_FILE_NAME-\${artifact_version}.zip" -d "$ZIP_FILE_NAME-\${artifact_version}"

                        ls -ltr
                        cd $ZIP_FILE_NAME-\${artifact_version}
                        func azure functionapp publish ${params.AZURE_FUNCTION_NAME} --python
                        az logout
                    """
                }
            }
        }

        /*
        stage('Deploy Code to Azure Function App') {
            steps {
                script {


                    // install azure-functions-core-tools install
                    wget https://github.com/Azure/azure-functions-core-tools/releases/download/4.0.5455/Azure.Functions.Cli.linux-x64.4.0.5455.zip
                    unzip -o -d azure-functions-cli Azure.Functions.Cli.linux-x64.*.zip
                    cd azure-functions-cli
                    chmod +x func
                    chmod +x gozip
                    export PATH=`pwd`:$PATH
                    cd ..

                    sh """
                    ls -ltr
                    cd 
                    func azure functionapp publish ${params.AZURE_FUNCTION_NAME} --python
                    """
                }
            }
        } */
 
    }
}