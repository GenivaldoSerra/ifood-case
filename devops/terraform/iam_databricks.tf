resource "aws_iam_user" "databricks_user" {
  name = "nyc-trip-record-databricks"

  tags = {
    project = "nyc-trip-record"
    purpose = "databricks-integration"
  }
}

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

data "aws_iam_policy_document" "oidc_manage_keys" {
  statement {
    actions = [
      "iam:CreateAccessKey",
      "iam:DeleteAccessKey",
      "iam:ListAccessKeys"
    ]
    resources = [
      aws_iam_user.databricks_user.arn
    ]
  }
}

resource "aws_iam_policy" "oidc_manage_keys" {
  name        = "nyc-trip-record-oidc-manage-databricks-keys"
  description = "Allow OIDC role to manage access keys for Databricks user"
  policy      = data.aws_iam_policy_document.oidc_manage_keys.json
}

data "aws_iam_role" "nyc_trip_record_oidc" {
  name = "nyc-trip-record-oidc"
}

resource "aws_iam_role_policy_attachment" "oidc_attach_manage_keys" {
  role       = data.aws_iam_role.nyc_trip_record_oidc.name
  policy_arn = aws_iam_policy.oidc_manage_keys.arn
}

resource "aws_s3_bucket" "bucket" {
  bucket = "nyc-trip-record-ifood"

  tags = {
    component   = "setup"
    cost_center = "nyc_trip_record"
    developer   = "calilisantos@gmail.com"
    env         = "dev"
    resource    = "nyc_trip_record_bucket"
  }
}

resource "aws_s3_object" "folders" {
  for_each = toset(["raw/", "refined/", "trusted/"])

  bucket  = aws_s3_bucket.bucket.id
  key     = each.key
  content = ""
  tags = aws_s3_bucket.bucket.tags
}
