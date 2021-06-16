from checkov.common.models.enums import CheckCategories
from checkov.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from checkov.common.models.consts import ANY_VALUE


class BackupVaultEncrypted(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure Backup Vault server-side encryption is enabled."
        id = "CKV_AWS_165"
        supported_resources = ['aws_backup_vault']
        categories = [CheckCategories.BACKUP_AND_RECOVERY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'kms_key_arn'

    def get_expected_value(self):
        return ANY_VALUE

check = BackupVaultEncrypted()