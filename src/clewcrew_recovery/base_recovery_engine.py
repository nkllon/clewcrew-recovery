#!/usr/bin/env python3
"""
Base Recovery Engine for clewcrew
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator


class RecoveryResult(BaseModel):
    """Result from recovery action"""

    success: bool
    message: str = Field(default="Recovery completed")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    changes_made: List[str] = Field(default_factory=list)
    engine_name: str = Field(default="unknown")
    files_fixed: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v):
        """Ensure confidence is between 0.0 and 1.0."""
        return max(0.0, min(1.0, v))


class BaseRecoveryEngine(ABC):
    """Base class for all recovery engines"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.engine_type = self.__class__.__name__

    @abstractmethod
    async def execute_recovery(self, action: Dict[str, Any]) -> RecoveryResult:
        """Execute recovery action"""
        pass

    def get_recovery_actions(self) -> List[str]:
        """Get list of available recovery actions for this engine"""
        return ["default_recovery"]

    def validate_action(self, action: Dict[str, Any]) -> bool:
        """Validate that the action is valid for this engine"""
        required_fields = ["target_files"]
        return all(field in action for field in required_fields)

    def calculate_confidence(self, errors: List[str], warnings: List[str]) -> float:
        """Calculate confidence score based on errors and warnings"""
        base_confidence = 0.8

        # Penalize for errors
        if errors:
            base_confidence -= len(errors) * 0.1

        # Slight penalty for warnings
        if warnings:
            base_confidence -= len(warnings) * 0.05

        return max(0.0, min(1.0, base_confidence))
