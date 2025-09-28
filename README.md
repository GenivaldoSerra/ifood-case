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


* Criar external location:

Boa, Calili 🚀 já temos os dados no bucket 🎉 Agora vamos organizar o **catálogo e schemas** no Databricks para consumir esses arquivos como tabelas externas. Vou te enumerar os passos do fluxo completo:

---

### **1. Criar a External Location**

Na **free edition** do Databricks, você provavelmente não conseguirá rodar o comando `CREATE EXTERNAL LOCATION` direto no SQL, porque isso exige Unity Catalog + admin.
👉 Alternativas:

* **(A)** Criar via **AWS Quickstart** (ele provisiona a role + external location automaticamente).
* **(B)** Se não der, você pode **usar apenas credenciais via secrets** (como já fez) e acessar o bucket diretamente no Spark.

Mas o ideal (se tiver suporte UC ativado) seria:

```sql
CREATE EXTERNAL LOCATION nyc_trip_location
URL 's3://nyc-trip-record-ifood/raw'
WITH (STORAGE CREDENTIAL aws_credential);
```

Onde `aws_credential` é configurado via:

```sql
CREATE STORAGE CREDENTIAL aws_credential
WITH AWS_ACCESS_KEY_ID = '{{seu_access_key}}'
AWS_SECRET_ACCESS_KEY = '{{seu_secret_key}}';
```

⚠️ No **free**, isso provavelmente não vai rolar — então você usará `dbutils.fs.mount` ou apenas path direto `s3://...`.

---

### **2. Criar o Catálogo**

Mesmo sem external location, você consegue criar o catálogo para organizar os schemas.
O catálogo precisa de uma pasta managed (mas pode ser só a raiz do bucket, já que você não vai usar tabelas managed agora).

```sql
CREATE CATALOG nyc_trip_catalog
MANAGED LOCATION 's3://nyc-trip-record-ifood/';
```

---

### **3. Criar os Schemas**

Criamos três camadas (`raw`, `trusted`, `refined`).
No caso de external tables, vamos associar cada schema a uma pasta:

```sql
CREATE SCHEMA nyc_trip_catalog.raw
MANAGED LOCATION 's3://nyc-trip-record-ifood/raw';

CREATE SCHEMA nyc_trip_catalog.trusted
MANAGED LOCATION 's3://nyc-trip-record-ifood/trusted';

CREATE SCHEMA nyc_trip_catalog.refined
MANAGED LOCATION 's3://nyc-trip-record-ifood/refined';
```

---

### **4. Criar as Tabelas Externas (por cor de táxi)**

Como você já organizou os arquivos em pastas (`fhv`, `fhvhv`, `green`, `yellow`), dá pra criar uma tabela para cada.
No SQL:

```sql
USE CATALOG nyc_trip_catalog;
USE SCHEMA raw;

-- Tabela FHV
CREATE TABLE fhv
USING PARQUET
LOCATION 's3://nyc-trip-record-ifood/raw/fhv/';

-- Tabela FHVHV
CREATE TABLE fhvhv
USING PARQUET
LOCATION 's3://nyc-trip-record-ifood/raw/fhvhv/';

-- Tabela Green
CREATE TABLE green
USING PARQUET
LOCATION 's3://nyc-trip-record-ifood/raw/green/';

-- Tabela Yellow
CREATE TABLE yellow
USING PARQUET
LOCATION 's3://nyc-trip-record-ifood/raw/yellow/';
```

---

### **5. Testar as Consultas**

Depois é só rodar no SQL do Databricks:

```sql
SELECT COUNT(*) FROM nyc_trip_catalog.raw.green;
SELECT * FROM nyc_trip_catalog.raw.yellow LIMIT 10;
```

---

### **Resumo dos passos na ordem**

1. (Opcional) Criar External Location via Quickstart (se conseguir).
2. Criar catálogo apontando para o bucket raiz.
3. Criar schemas (`raw`, `trusted`, `refined`) apontando para subpastas.
4. Criar tabelas externas por cor de táxi (`fhv`, `fhvhv`, `green`, `yellow`).
5. Testar queries para validar acesso.

---

👉 Pergunta pra ti:
Quer que eu já monte **uma versão “plano B” sem Unity Catalog**, só com `spark.read.parquet("s3://...")` e depois `saveAsTable`? Assim você não depende do `CREATE EXTERNAL LOCATION`.
