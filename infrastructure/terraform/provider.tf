provider "azurerm" {
  features {
  }
  use_oidc                        = false
  resource_provider_registrations = "none"
  subscription_id                 = "adfbd062-5306-44fc-943f-f14d4442c98e"
  environment                     = "public"
  use_msi                         = false
  use_cli                         = true
}
