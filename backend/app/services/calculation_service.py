"""
Coconut calculation service implementing the business logic.
"""
import uuid
from typing import List
from datetime import datetime

from app.models.calculation import (
    CalculationInput, 
    CalculationResult, 
    CalculationStep,
    CalculationSummary
)


class CoconutCalculationService:
    """Service class for performing coconut vendor calculations."""
    
    def __init__(self):
        self.calculations_history: List[CalculationResult] = []
    
    def calculate(self, input_data: CalculationInput) -> CalculationResult:
        """
        Perform the complete coconut calculation.
        
        Args:
            input_data: Input parameters for calculation
            
        Returns:
            Complete calculation result with breakdown
        """
        calculation_steps = []
        step_counter = 1
        
        # Step 1: Calculate wastage
        wastage_coconuts = int(input_data.total_coconuts * (input_data.wastage_percentage / 100))
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Wastage Deduction",
            calculation=f"{input_data.total_coconuts} × {input_data.wastage_percentage}% = {wastage_coconuts}",
            result=wastage_coconuts
        ))
        step_counter += 1
        
        # Step 2: Calculate sellable coconuts
        sellable_coconuts = input_data.total_coconuts - wastage_coconuts
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Sellable Coconuts",
            calculation=f"{input_data.total_coconuts} - {wastage_coconuts} = {sellable_coconuts}",
            result=sellable_coconuts
        ))
        step_counter += 1
        
        # Step 3: Calculate gross revenue
        gross_revenue = sellable_coconuts * input_data.price_per_coconut
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Gross Revenue",
            calculation=f"{sellable_coconuts} × ₹{input_data.price_per_coconut} = ₹{gross_revenue:,.0f}",
            result=gross_revenue
        ))
        step_counter += 1
        
        # Step 4: Calculate tax amount
        tax_amount = gross_revenue * (input_data.tax_percentage / 100)
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Tax Deduction",
            calculation=f"₹{gross_revenue:,.0f} × {input_data.tax_percentage}% = ₹{tax_amount:,.0f}",
            result=tax_amount
        ))
        step_counter += 1
        
        # Step 5: Calculate after-tax revenue
        after_tax_revenue = gross_revenue - tax_amount
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="After-Tax Revenue",
            calculation=f"₹{gross_revenue:,.0f} - ₹{tax_amount:,.0f} = ₹{after_tax_revenue:,.0f}",
            result=after_tax_revenue
        ))
        step_counter += 1
        
        # Step 6: Calculate labor cost (based on original total coconuts)
        labor_cost = input_data.total_coconuts * (input_data.labor_percentage / 100)
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Labor Cost",
            calculation=f"{input_data.total_coconuts} × {input_data.labor_percentage}% = ₹{labor_cost:,.0f}",
            result=labor_cost
        ))
        step_counter += 1
        
        # Step 7: Calculate final net profit
        net_profit = after_tax_revenue - labor_cost
        calculation_steps.append(CalculationStep(
            step=step_counter,
            description="Net Profit",
            calculation=f"₹{after_tax_revenue:,.0f} - ₹{labor_cost:,.0f} = ₹{net_profit:,.0f}",
            result=net_profit
        ))
        
        # Calculate profit margin percentage
        profit_margin_percentage = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0
        
        # Create calculation result
        result = CalculationResult(
            input_data=input_data,
            wastage_coconuts=wastage_coconuts,
            sellable_coconuts=sellable_coconuts,
            gross_revenue=gross_revenue,
            tax_amount=tax_amount,
            after_tax_revenue=after_tax_revenue,
            labor_cost=labor_cost,
            net_profit=net_profit,
            profit_margin_percentage=profit_margin_percentage,
            calculation_steps=calculation_steps,
            calculation_id=str(uuid.uuid4()),
            created_at=datetime.now()
        )
        
        # Store in history
        self.calculations_history.append(result)
        
        return result
    
    def get_calculation_summary(self, result: CalculationResult) -> CalculationSummary:
        """
        Get a summary view of the calculation.
        
        Args:
            result: Complete calculation result
            
        Returns:
            Summary of the calculation
        """
        return CalculationSummary(
            total_coconuts=result.input_data.total_coconuts,
            price_per_coconut=result.input_data.price_per_coconut,
            gross_revenue=result.gross_revenue,
            net_profit=result.net_profit,
            profit_margin_percentage=result.profit_margin_percentage,
            created_at=result.created_at
        )
    
    def get_calculations_history(self) -> List[CalculationSummary]:
        """
        Get history of all calculations.
        
        Returns:
            List of calculation summaries
        """
        return [self.get_calculation_summary(calc) for calc in self.calculations_history]
    
    def validate_input(self, input_data: CalculationInput) -> List[str]:
        """
        Validate input data and return list of errors if any.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        try:
            input_data.dict()  # This will trigger Pydantic validation
        except Exception as e:
            errors.append(str(e))
        
        # Additional business logic validation
        if input_data.total_coconuts > 1000000:
            errors.append("Total coconuts seems unusually high (> 1,000,000)")
        
        if input_data.price_per_coconut > 1000:
            errors.append("Price per coconut seems unusually high (> ₹1,000)")
        
        if input_data.wastage_percentage > 50:
            errors.append("Wastage percentage seems unusually high (> 50%)")
        
        return errors