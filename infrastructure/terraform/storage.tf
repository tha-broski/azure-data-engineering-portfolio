resource "azurerm_storage_account" "adls" {
  account_replication_type        = "LRS"
  account_tier                    = "Standard"
  allow_nested_items_to_be_public = false
  default_to_oauth_authentication = true
  is_hns_enabled                  = true
  location                        = var.location
  name                            = var.storage_account_name
  resource_group_name             = var.resource_group_name
  tags = {
    environment = "dev"
    owner       = "tha-broski"
    project     = "data-engineering-portfolio"
    purpose     = "portfolio"
  }
}
