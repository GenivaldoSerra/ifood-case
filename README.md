## **Requisitos:**
* Fazer fork desse projeto
* Conta AWS
* Conta Databricks Free Edition
* Criar PAT Databricks (no cenário de usar Databricks API nos workflows Github Actions)
* Clonar repositório no Databricks (validar se tem endpoint no Databricks API para isso)
  Endpoint: https://docs.databricks.com/api/workspace/repos/create
  * How to: (sumário)
* Configurar conexão Github<>Terraform:
  * Criar OIDC (OpenID Connect):
    * Referência [aqui](https://aws.amazon.com/pt/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/)
    * Necessário:
      * Informar nome do seu perfil no campo `Github Organization` , na criação da função (role) do OIDC, conforme a referência acima (Step 2);
      * Coloque `NycTripRecordOidcRole` como nome da role na criação da função (role) do OIDC, conforme a referência acima (Step 2);
      * Selecione a role: `AmazonS3FullAccess` na criação da função (role) do OIDC, conforme a referência acima (Step 2);
    * Recomendado:
      * Informar url do repositório que foi feito o fork, na criação da função (role) do OIDC, conforme a referência acima
      * Colocar tags desse projeto;
      * Especificar branch do repositório que foi feito o fork, na criação da função (role) do OIDC, conforme a referência acima
  * Adicionar `ARN` do Identity Provider criado nas variáveis do repositório criado
    * No seu repositório acesse:
      * Aba `Settings` 
      * Na seção `Security`, clique em `Secrets and variables` 
      *Clique em `Actions` 
      * Na sequência, clique na aba `Variables` 
      * Crie uma variável com o nome `NYC_TRIP_RECORD_OIDC_ARN`, com o valor do ARN do Identity Provider criado
      * Crie uma variável com o nome `NYC_TRIP_RECORD_AWS_REGION` com o valor us-east-2
    * **IMPORTANTE:** os nomes acima e a criação dessas variáveis é necessário para deploy do S3 que utiliza essas configurações

* Configurar conexão AWS<>Databricks Free Edition 
  * Limitações (para ADR): Instance profile precisa de databricks provisionado na AWS: https://docs.databricks.com/aws/pt/connect/storage/tutorial-s3-instance-profile
  * Storage credential e external location tem restrições tambem. Criação delas foi feita com sucesso através do AWS Quickstart (que utiliza CloudFormation)
  * Opção: criar access_key e access_secret_key e colocar como secret no Databricks



      * Procure por `IAM` e abra o menu
      * No menu IAM, busque por `Identity Providers (ou Provedores de Identidade)`
      * No menu de Identity Providers, clique em `Adicionar provedor`
      * No menu de Adicionar provedor de identidade especifique:
        * `OpenID Connect` como Tipo de provedor
        * informe um nome de provedor
    * No Databricks:
      * No seu perfil (ícone superior à direita com a letra inicial do seu nome de perfil), acessar:
        * Settings > Compute > Botão `Manage` ao lado de SQL warehouses and serverless compute > 