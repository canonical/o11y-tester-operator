module "ssc" {
  source = "git::https://github.com/canonical/self-signed-certificates-operator//terraform"
  model  = var.model
}

variable "model" {
  type = string
}