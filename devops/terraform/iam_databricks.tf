# Usuário para integração com Databricks
resource "aws_iam_user" "databricks_user" {
  name = "nyc-trip-record-databricks"

  tags = {
    project = "nyc-trip-record"
    purpose = "databricks-integration"
  }
}

# Policy de acesso ao bucket S3
data "aws_iam_policy_document" "databricks_bucket_access" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::nyc-trip-record-ifood",
      "arn:aws:s3:::nyc-trip-record-ifood/*"
    ]
  }
}

resource "aws_iam_policy" "databricks_bucket_access" {
  name        = "nyc-trip-record-databricks-s3"
  description = "Allow Databricks user to access nyc-trip-record-ifood bucket"
  policy      = data.aws_iam_policy_document.databricks_bucket_access.json
}

resource "aws_iam_user_policy_attachment" "databricks_attach_bucket" {
  user       = aws_iam_user.databricks_user.name
  policy_arn = aws_iam_policy.databricks_bucket_access.arn
}

# Referência à role OIDC existente
data "aws_iam_role" "nyc_trip_record_oidc" {
  name = "nyc-trip-record-oidc" # ajuste para o nome exato da role no AWS Console
}

# Policy inline diretamente na role OIDC para gerenciar as keys do usuário Databricks
resource "aws_iam_role_policy" "oidc_manage_databricks_keys" {
  name = "nyc-trip-record-oidc-manage-databricks-keys"
  role = data.aws_iam_role.nyc_trip_record_oidc.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:CreateAccessKey",
          "iam:DeleteAccessKey",
          "iam:ListAccessKeys"
        ]
        Resource = aws_iam_user.databricks_user.arn
      }
    ]
  })
}
