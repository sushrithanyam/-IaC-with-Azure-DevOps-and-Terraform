resource "azurerm_resource_group" "rg" {
  name     = "cloudtask-rg"
  location = "centralus"

  tags = var.tags
}