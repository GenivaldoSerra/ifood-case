resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    { env = var.env }
  )
}

resource "aws_s3_object" "folders" {
  for_each = toset(var.bucket_folders)

  bucket = aws_s3_bucket.bucket.id
  key    = "${each.value}/"

  tags = merge(
    var.tags,
    { env = var.env }
  )
}
