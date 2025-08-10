# 🥥 CocoLedger Backend CLI

A Python-based command-line interface for calculating coconut vendor profits with beautiful output formatting.

## 📋 Features

- **Accurate Calculations**: Implements the exact coconut vendor calculation logic
- **Beautiful CLI**: Rich formatting with tables and colors
- **Multiple Input Methods**: Command-line arguments or interactive prompts
- **Input Validation**: Comprehensive validation with helpful error messages
- **Calculation History**: Track multiple calculations (within session)
- **Step-by-Step Breakdown**: Detailed calculation steps for transparency

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Option 1: Convenience Script (Recommended)

```bash
# Show all available commands
./run_calculator.sh

# Run example calculation
./run_calculator.sh example

# Interactive mode
./run_calculator.sh interactive

# Direct calculation
./run_calculator.sh calculate --coconuts 10000 --price 20
```

#### Option 2: Direct Python Command

```bash
# Activate virtual environment first
source venv/bin/activate

# Run example
python coconut_calculator_cli.py example

# Interactive mode
python coconut_calculator_cli.py interactive

# Help
python coconut_calculator_cli.py --help
```

## 📊 Calculation Logic

The CLI implements the following calculation flow:

1. **Wastage Deduction** (default 2.2%)

   - Wastage Coconuts = Total Coconuts × Wastage %
   - Sellable Coconuts = Total Coconuts - Wastage Coconuts

2. **Revenue Calculation**

   - Gross Revenue = Sellable Coconuts × Price per Coconut

3. **Tax Deduction** (default 1%)

   - Tax Amount = Gross Revenue × Tax %
   - After-Tax Revenue = Gross Revenue - Tax Amount

4. **Labor Cost** (default 11% of original quantity)

   - Labor Cost = Total Coconuts × Labor %

5. **Final Profit**
   - Net Profit = After-Tax Revenue - Labor Cost

## 🎯 Example Calculation

**Input:**

- Total Coconuts: 10,000
- Price per Coconut: ₹20
- Wastage: 2.2%
- Tax: 1%
- Labor: 11%

**Output:**

- Wastage: 220 coconuts
- Sellable: 9,780 coconuts
- Gross Revenue: ₹195,600
- Tax Amount: ₹1,956
- Labor Cost: ₹1,100
- **Net Profit: ₹192,544**

## 🛠️ CLI Commands

### `example`

Runs the predefined example calculation and verifies against expected results.

```bash
./run_calculator.sh example
```

### `calculate`

Performs calculation with specified parameters.

```bash
# Using command-line arguments
./run_calculator.sh calculate --coconuts 5000 --price 25 --wastage 3 --tax 1.5 --labor 12

# Interactive mode (prompts for input)
./run_calculator.sh calculate
```

**Parameters:**

- `--coconuts, -c`: Total number of coconuts (required)
- `--price, -p`: Price per coconut in rupees (required)
- `--wastage, -w`: Wastage percentage (default: 2.2)
- `--tax, -t`: Tax percentage (default: 1.0)
- `--labor, -l`: Labor percentage (default: 11.0)

### `interactive`

Starts an interactive session where you can perform multiple calculations.

```bash
./run_calculator.sh interactive
```

### `history`

Shows calculation history for the current session.

```bash
./run_calculator.sh history
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── calculation.py          # Data models
│   ├── services/
│   │   ├── __init__.py
│   │   └── calculation_service.py  # Business logic
│   └── __init__.py
├── coconut_calculator_cli.py       # CLI interface
├── run_calculator.sh              # Convenience script
├── requirements.txt               # Dependencies
└── README.md                     # This file
```

## 🔧 Development

### Dependencies

- **pydantic**: Data validation and modeling
- **click**: Command-line interface framework
- **rich**: Beautiful terminal output
- **fastapi**: (Future web API support)
- **uvicorn**: (Future web server support)

### Testing

The CLI includes built-in validation testing:

```bash
# Test with the original example
./run_calculator.sh example

# Test with different parameters
./run_calculator.sh calculate --coconuts 1000 --price 30

# Test validation (try invalid inputs)
./run_calculator.sh calculate --coconuts -100 --price 0
```

## 📈 Future Enhancements

This CLI serves as the foundation for the web application and includes:

- ✅ Complete calculation logic
- ✅ Input validation
- ✅ Error handling
- ✅ Beautiful output formatting
- ✅ Multiple input methods

**Planned Features:**

- Database persistence
- Web API endpoints
- User authentication
- Calculation export (PDF/Excel)
- Historical data analysis

## 🐛 Troubleshooting

### Common Issues

1. **ImportError**: Make sure virtual environment is activated

   ```bash
   source venv/bin/activate
   ```

2. **Permission Denied**: Make scripts executable

   ```bash
   chmod +x run_calculator.sh coconut_calculator_cli.py
   ```

3. **Module Not Found**: Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## 📄 License

This project is part of the CocoLedger application for coconut vendor profit calculations.

---

**Created for coconut vendors to easily calculate their profits with accuracy and transparency.**
