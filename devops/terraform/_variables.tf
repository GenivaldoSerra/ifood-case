variable "bucket_folders" {
  type    = list(string)
  default = ["raw", "refined", "trusted"]
}

variable "bucket_name" {
  type    = string
  default = "nyc-trip-record"
}

variable "env" {
  type = string
}

variable "tags" {
  type = map(string)
  default = {
    component   = "setup"
    cost_center = "nyc_trip_record"
    developer   = "calilisantos@gmail.com"
    resource    = "nyc_trip_record_bucket"
  }
}
