from __future__ import annotations

from typing import Any
from abc import abstractmethod

from jsonpath_ng import parse

from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.github.base_github_configuration_check import BaseGithubCheck
from checkov.github.schemas.branch_protection import schema as branch_security_schema
from checkov.github.schemas.no_branch_protection import schema as no_branch_security_schema
from checkov.json_doc.enums import BlockType

MESSAGE_BRANCH_NOT_PROTECTED = 'Branch not protected'


class BranchSecurity(BaseGithubCheck):
    def __init__(self, id: str, name: str) -> None:
        categories = (CheckCategories.SUPPLY_CHAIN,)
        super().__init__(
            id=id,
            name=name,
            categories=categories,
            supported_entities=("*",),
            block_type=BlockType.DOCUMENT,
        )

    def scan_entity_conf(self, conf: dict[str, Any], entity_type: str) -> CheckResult | None:  # type:ignore[override]
        if branch_security_schema.validate(conf):
            jsonpath_expression = parse("$..{}".format(self.get_evaluated_keys()[0].replace("/", ".")))
            matches = jsonpath_expression.find(conf)
            if matches and all(isinstance(match.value, dict) or match.value == self.get_expected_value() for match in matches):
                return CheckResult.PASSED
            else:
                return CheckResult.FAILED
        if no_branch_security_schema.validate(conf):
            message = conf.get('message', '')
            if message == MESSAGE_BRANCH_NOT_PROTECTED:
                return CheckResult.FAILED
        return None

    def get_expected_value(self) -> str | bool:
        return True

    @abstractmethod
    def get_evaluated_keys(self) -> list[str]:
        pass
