module "cos-lite" {
  source       = "git::https://github.com/canonical/observability-stack//terraform/cos-lite"
  model        = var.model
  channel      = var.channel
  internal_tls = var.internal_tls
}

variable "model" {
  type = string
}

variable "channel" {
  type = string
}

variable "internal_tls" {
  type    = bool
  default = true
}

variable "external_certificates_offer_url" {
  type    = string
  default = null
}
