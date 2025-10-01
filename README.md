# Boas vindas ao **ifood-case!**

Para executar o projeto, observe as orientações descritas a seguir, e se tiver qualquer dúvida, sugestão, contribuição, considere abrir uma issue ou entrar em contato. 🚀

Aqui você vai encontrar os detalhes de como está estruturado e foi desenvolvido o projeto.

# <a id='topicos'>Tópicos</a>
- [Desenvolvimento](#desenvolvimento)
  - [Objetivo](#objetivo)
  - [Estrutura do projeto](#estrutura)
  - [Tecnologias utilizadas](#tecnologias)
- [Orientações](#orientacoes)
  - [Executando o projeto](#execucao)
- [Implementações](#implementacoes)
  - [Contextualizando](#contextualizando)
  - [Continuous Delivery](#ci)
    - [NYC Bucket Setup](#bs)
    - [Databricks Setup](#db)
  - [Camada de Consumo](#cl)
    - [Desenho do ambiente](#layers)
    - [Modelagem de Dados](#der)
- [Decisões Arquiteturais](#adr)
  - [Definições de Solução](#c4-model)
  - [Registros de Decisão](#registros)
- [Próximos passos](#next)

# <a id='desenvolvimento'>[Desenvolvimento](#topicos)</a>

<strong><a id='objetivo'>[Objetivo](#topicos)</a></strong>

  O **objetivo** é construir um datalake com os dados da Taxi & Limousine Comission (TLC) de Nova York, disponíveis [aqui](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Em um primeiro recorte, com o sample de Janeiro a Maio de 2023.
  
  Para isso, foi definida uma [**arquitetura de referência**](#c4-model) e [**modelagem dos dados**](#der) tornando a disponibilidade e consumo do ambiente analítico escalável e resiliente.

  ---

<strong><a id='estrutura'>[Estrutura do projeto](#topicos)</a></strong>

* **Na pasta [.github](.github) estão os diretórios:**
  * **[actions](.github\actions)** com custom actions do `GitHub Actions`, modularizando e desaclopando steps dos workflows de subida dos componentes da arquitetura de referência;
  * **[workflows](.github\workflows)** com os workflows `GitHub Actions` que iniciam o setup das duas soluções adotadas para construção do datalake para o projeto:
    * **[databricks_setup](.github\workflows\databricks_setup.yml)** que adiciona as secrets, esse repositório e cria no ambiente Databricks informado, os jobs de ingestão e transformação de dados da TLC;
    * **[nyc_bucket_setup](.github\workflows\nyc_bucket_setup.yml)** que cria um bucket S3 no console AWS informado, para storage do datalake pavimentado pelo Databricks;
* **Na pasta [analysis](analysis) estão os arquivos que endereçam questões de negócio sobre os dados do TLC NYC**;
* **Na pasta [devops](devops) estão os módulos utilizados pelos workflows `GitHub Actions`** para pavimentação do Databricks e S3 (baseado em Terraform);
* **Na pasta [src](src) estão os diretórios:**
  * **[dataops](src\dataops)** com os códigos fonte utilizados para as operações do ambiente analítico, atualmente no processamento de dados específicos da origem que não puderam seguir o fluxo normal. Mais sobre o tema [aqui](#registros);
  * **[ingestion](src\ingestion)** com os códigos fonte do job de ingestão dos dados do TLC para a camada bruta (raw) de processamento;
  * **[transform](src\transform)** com os códigos fonte do job de transformações dos dados brutos e pouso nas camadas de consumo dos times de análise (refined e trusted);

  ---

<strong><a id='tecnologias'>[Tecnologias utilizadas](#topicos)</a></strong>

  O projeto foi desenvolvido utilizando o AWS S3 como solução de armazenamento dos dados, e o Databricks Free Edition como solução para aquisição, processamento e consumo (serving) no ambiente analítico.

  Para provisionamento do código, o `Github Actions` foi a solução utilizada para entrega e integração contínua da infraestrutura e desenvolvimento do ambiente. E o `Terraform` foi a opção empregada para versionamento e deploy da infraestrutura integral do S3.

  Ainda sobre o processamento dos dados, o `Python` foi utilizado como API principal, e as bibliotecas e engines utilizadas através do Databricks, baseadas no Python, foram as abaixo

  * **[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html):** Kit de desenvolvimento (SDK) da AWS que habilita via código ter uma interface programática com os recursos da cloud. Aqui utilizada como solução de aquisição de dados, dada a integração da ferramenta abaixo com processamento dos recursos
  * **[PySpark](https://spark.apache.org/docs/latest/api/python/index.html):** API em python do `Apache Spark`, que habilita através da linguagem o processamento de dados massivos (Big Data). É também solução primária no Databricks, que opera via Cluster Jobs do Spark toda a carga e recursos de rede utilizados no Databricks.

  ---

# <a id='orientacoes'>[Orientações](#topicos)</a>

<strong><a id='execucao'>[Executando o projeto](#topicos)</a></strong>


  ---

# <a id='implementacoes'>[Implementações](#topicos)</a>

<strong><a id='contextualizando'>[Contextualizando](#topicos)</a></strong>

<strong><a id='ci'>[Continuous Delivery](#topicos)</a></strong>

<strong><a id='bs'>[NYC Bucket Setup](#topicos)</a></strong>

<strong><a id='db'>[Databricks Setup](#topicos)</a></strong>

<strong><a id='cl'>[Camada de Consumo](#topicos)</a></strong>

<strong><a id='layers'>[Desenho do ambiente](#topicos)</a></strong>

<strong><a id='der'>[Modelagem de Dados](#topicos)</a></strong>


  ---

# <a id='adr'>[Decisões Arquiteturais](#topicos)</a>

<strong><a id='c4-model'>[Definições de Solução](#topicos)</a></strong>

<strong><a id='registros'>[Registros de Decisão](#topicos)</a></strong>


  ---

# <a id='next'>[Próximos passos](#topicos)</a>

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
  * Decisão: criar access_key e access_secret_key no Console AWS e colocar em secrets github

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


* Configurar ingestão
  * Documentar CloudFormation
  * Execução dos jobs de ingestão

* Decisão:
  Tirar período Janeiro-2023 da raw, dada inconsistência dos dados

* Evoluções:
  * Tabela de parâmetros, tornando ingestões dinâmicas (flag para ingerir ou não)
  * Testes de integração, unitários
  * Estratégia SCD 