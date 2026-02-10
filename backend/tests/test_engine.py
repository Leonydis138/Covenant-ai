"""Tests for Constitutional Engine"""
import pytest
from covenant.core.constitutional_engine import (
    AdvancedConstitutionalEngine,
    Action,
    Constraint,
    ConstraintType
)

@pytest.mark.asyncio
async def test_engine_evaluation():
    """Test basic engine evaluation"""
    engine = AdvancedConstitutionalEngine()
    
    action = Action(
        type="data_access",
        description="Access user records",
        actor="admin",
        parameters={"user_id": "123"}
    )
    
    result = await engine.evaluate_action(action)
    
    assert result.action_id == action.id
    assert isinstance(result.overall_score, float)
    assert 0 <= result.overall_score <= 1

@pytest.mark.asyncio
async def test_hard_constraint_violation():
    """Test hard constraint blocking"""
    engine = AdvancedConstitutionalEngine()
    
    # Add hard constraint
    constraint = Constraint(
        id="test_hard",
        type=ConstraintType.SAFETY,
        description="Test hard constraint",
        is_hard=True
    )
    engine.add_constraint(constraint, "SafetyLayer")
    
    action = Action(
        type="dangerous_action",
        parameters={"harm": 1.0}  # Will violate safety
    )
    
    result = await engine.evaluate_action(action)
    
    # Should be blocked by hard constraint
    assert result.is_allowed == False or len(result.violations) > 0

def test_metrics():
    """Test metrics collection"""
    engine = AdvancedConstitutionalEngine()
    metrics = engine.get_metrics()
    
    assert "total_evaluations" in metrics
    assert "average_score" in metrics
    assert metrics["total_evaluations"] == 0
