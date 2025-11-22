"""Tests for cost tracker."""
import pytest
from src.utils.cost_tracker import CostTracker


def test_cost_tracker_initialization():
    """Test tracker initializes correctly."""
    tracker = CostTracker()
    assert tracker.total_calls == 0
    assert tracker.total_tokens == 0


def test_cost_tracker_log_call():
    """Test logging API calls."""
    tracker = CostTracker()
    tracker.log_call(tokens=100)
    assert tracker.total_calls == 1
    assert tracker.total_tokens == 100
    
    tracker.log_call(tokens=50)
    assert tracker.total_calls == 2
    assert tracker.total_tokens == 150


def test_cost_tracker_summary():
    """Test getting summary."""
    tracker = CostTracker()
    tracker.log_call(tokens=1000)
    
    summary = tracker.get_summary()
    assert summary["total_calls"] == 1
    assert summary["total_tokens"] == 1000
    assert summary["estimated_cost_usd"] == 0.0  # Ollama is free


def test_cost_tracker_reset():
    """Test resetting tracker."""
    tracker = CostTracker()
    tracker.log_call(tokens=500)
    tracker.reset()
    
    assert tracker.total_calls == 0
    assert tracker.total_tokens == 0


def test_cost_tracker_string_representation():
    """Test string output."""
    tracker = CostTracker()
    tracker.log_call(tokens=200)
    
    output = str(tracker)
    assert "Total Calls:" in output
    assert "200" in output
