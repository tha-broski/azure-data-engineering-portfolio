resource "azurerm_mssql_server" "sql_server" {
  administrator_login = "CloudSA5d7b062b"
  location            = "polandcentral"
  name                = "sql-de-portfolio-dev"
  resource_group_name = "rg-data-engineering-portfolio-dev"
  tags = {
    environment = "dev"
    owner       = "tha-broski"
    project     = "data-engineering-portfolio"
    purpose     = "portfolio"
  }
  version = "12.0"
  azuread_administrator {
    login_username = "dabrowskimarcin2001@gmail.com"
    object_id      = "e595f575-aa51-47a1-8989-8d15e08c589d"
    azuread_authentication_only = true
  }
}
resource "azurerm_mssql_database" "adventureworkslt" {
  name      = var.sql_database_name
  server_id = azurerm_mssql_server.sql_server.id
  storage_account_type = "Local"
  tags = {
    environment = "dev"
    owner       = "tha-broski"
    project     = "data-engineering-portfolio"
    purpose     = "portfolio"
  }
}

