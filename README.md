## **Requisitos:**
* Fazer fork desse projeto
* Conta AWS
* Conta Databricks Free Edition

* Clonar repositório no Databricks (validar se tem endpoint no Databricks API para isso)
  Endpoint: https://docs.databricks.com/api/workspace/repos/create
  * How to: (sumário)
* Parâmetros/Credenciais a criar:
  * AWS Console:
    * Access Key (Chave de Acesso)
    * Instance Provider (Provedor de Instância)
    * Role para o Instance Provider com o nome `NycTripRecordOidcRole` 
      > IMPORTANTE: É necessário usar esse nome para funcionamento da criação do S3
  * Databricks:
    * Personal Access Token (PAT) do Databricks
  * Github:
    * Repository Secrets:
      * AWS_ACCESS_KEY_ID: Com esse nome, e valor da access key da AWS criada
      * AWS_SECRET_ACCESS_KEY: Com esse nome, e valor da access key secret da AWS criada
      * DATABRICKS_TOKEN: Com esse nome, e valor do PAT Databricks
      * NYC_TRIP_RECORD_OIDC_ROLE_ARN: Com esse nome, e valor do ARN da Role do Instance Provider criada
* Parâmetros a informar:
  * Workflow Databricks Setup:
    * databricks_host: Url do Databricks antes do parâmetro "?o=<número_workspace>
      * Ex: url: https://dbc-ab3dba61-89cc.cloud.databricks.com/?o=3912183202474156; databricks_host: https://dbc-ab3dba61-89cc.cloud.databricks.com/
    * databricks_user_email: Seu email utilizado para login no Workspace Databricks
  * Workflow NYC Trip Record S3 Setup:
    * environment: Com os valores 'dev' ou 'prod' (a ser implementado)
    * aws_region: Com o valor da região a criar o bucket S3
      > IMPORTANTE: Para a versão free do Databricks, usar a região us-east-2 para funcionamento da integração AWS <> Databricks
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




### **Passo 1 – Entrar no IAM**

1. Acesse o console da AWS.
2. Vá em **IAM → Users**.
3. Clique no usuário que você quer usar (ex: `nyc-trip-record-databricks`).

   > Se não existir, crie o usuário primeiro:
   >
   > * User name: `nyc-trip-record-databricks`
   > * Access type: **Programmatic access** (necessário para boto3/CLI)
   > * Não esqueça de adicionar ao menos permissões para o bucket S3 que você vai usar.



### **Passo 2 – Criar Access Key**

1. Dentro do usuário, clique na aba **Security credentials**.
2. Role até **Access keys**.
3. Clique em **Create access key**.
4. Escolha **Programmatic access** e confirme.
5. Você verá **Access Key ID** e **Secret Access Key** — **salve em local seguro**, pois o Secret só aparece uma vez.

---

### **Passo 3 – Salvar no GitHub Secrets**

No repositório do GitHub:

1. Vá em **Settings → Secrets and variables → Actions → New repository secret**.
2. Crie dois secrets:

   * `AWS_ACCESS_KEY_ID` → cole o Access Key ID
   * `AWS_SECRET_ACCESS_KEY` → cole o Secret Access Key


