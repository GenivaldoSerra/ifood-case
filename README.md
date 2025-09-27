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
  * Adicionar `ARN` do Identity Provider criado, na Environment Secrets do repositório criado
    * No seu repositório acesse:
      * Aba `Settings` > Na seção `Environments`, clique em `New environment` > Crie um environment com o nome `dev` > Na sequência, clique em `Add environment secret` > Crie uma secret com o nome `NYC_TRIP_RECORD_OIDC_ARN`, com o valor do ARN do Identity Provider criado
* Configurar conexão AWS<>Databricks Free Edition 
  * How to: (sumário)
  * Obter o `workspace_id` do Databricks:
    * Na url após seu login na Free Edition, o id do workspace é o valor após o parâmetro `o=`. Exemplo:
      * **url:** https://dbc-ec2dba61-89cc.cloud.databricks.com/?o=2345678
      * **workspace_id:** 2345678
  * Criar Instance Profile:
    * Na AWS:
      * Procure por `IAM` e abra o menu
      * No menu IAM, busque por `Identity Providers (ou Provedores de Identidade)`
      * No menu de Identity Providers, clique em `Adicionar provedor`
      * No menu de Adicionar provedor de identidade especifique:
        * `OpenID Connect` como Tipo de provedor
        * informe um nome de provedor
    * No Databricks:
      * No seu perfil (ícone superior à direita com a letra inicial do seu nome de perfil), acessar:
        * Settings > Compute > Botão `Manage` ao lado de SQL warehouses and serverless compute > 