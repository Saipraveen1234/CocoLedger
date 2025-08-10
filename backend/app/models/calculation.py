"""
Calculation models for coconut vendor calculations.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class CalculationInput(BaseModel):
    """Input data for coconut calculation."""
    total_coconuts: int = Field(..., gt=0, description="Total number of coconuts")
    price_per_coconut: float = Field(..., gt=0, description="Price per coconut in rupees")
    wastage_percentage: float = Field(default=2.2, ge=0, le=100, description="Wastage percentage")
    tax_percentage: float = Field(default=1.0, ge=0, le=100, description="Tax percentage")
    labor_percentage: float = Field(default=11.0, ge=0, le=100, description="Labor percentage")

    @validator('total_coconuts')
    def validate_total_coconuts(cls, v):
        if v <= 0:
            raise ValueError('Total coconuts must be greater than 0')
        return v

    @validator('price_per_coconut')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price per coconut must be greater than 0')
        return v


class CalculationStep(BaseModel):
    """Individual calculation step for breakdown."""
    step: int = Field(..., description="Step number")
    description: str = Field(..., description="Description of the calculation step")
    calculation: str = Field(..., description="Mathematical calculation performed")
    result: float = Field(..., description="Result of this step")


class CalculationResult(BaseModel):
    """Complete calculation result with breakdown."""
    # Input data
    input_data: CalculationInput
    
    # Intermediate calculations
    wastage_coconuts: int = Field(..., description="Number of coconuts lost to wastage")
    sellable_coconuts: int = Field(..., description="Number of coconuts available for sale")
    gross_revenue: float = Field(..., description="Total revenue before deductions")
    tax_amount: float = Field(..., description="Tax amount to be deducted")
    after_tax_revenue: float = Field(..., description="Revenue after tax deduction")
    labor_cost: float = Field(..., description="Labor cost based on total coconuts")
    
    # Final results
    net_profit: float = Field(..., description="Final profit after all deductions")
    profit_margin_percentage: float = Field(..., description="Profit margin as percentage")
    
    # Calculation breakdown
    calculation_steps: List[CalculationStep] = Field(..., description="Step-by-step calculation breakdown")
    
    # Metadata
    calculation_id: Optional[str] = Field(None, description="Unique calculation identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Calculation timestamp")


class CalculationSummary(BaseModel):
    """Summary view of calculation for display."""
    total_coconuts: int
    price_per_coconut: float
    gross_revenue: float
    net_profit: float
    profit_margin_percentage: float
    created_at: datetime