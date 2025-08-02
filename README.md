# Personal Expense Tracker

A comprehensive command-line expense tracking application built in Python that helps you manage your personal finances with ease.

## 📋 Features

### Core Features
- ✅ **Add & Manage Expenses** - Track expenses with amount, description, category, and payment method
- ✅ **Category Management** - Customizable expense categories (Food, Transport, Utilities, etc.)
- ✅ **Payment Method Tracking** - Track expenses by Cash, UPI, or Card
- ✅ **Date-based Filtering** - Filter expenses by month and year
- ✅ **Balance Management** - Track bank and cash balances with history
- ✅ **Data Persistence** - Automatic saving of all data to local files

### Analysis & Reporting
- 📊 **Monthly Summary** - Category-wise expense breakdown
- 📈 **Budget Alerts** - Set monthly budgets and get alerts
- 🔍 **Highest Expense Tracking** - Find your biggest expenses
- 📋 **Detailed Listing** - View all expenses with full details
- 📊 **Export Functionality** - Export data to CSV files

### Data Management
- 💾 **Memory System** - Recent expenses stored separately
- 🔄 **Edit & Delete** - Modify or remove existing entries
- 📁 **File Export** - Generate detailed expense reports
- 🗂️ **Data Backup** - Automatic data persistence

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher (uses dataclasses)
- pip package manager

### Quick Start
1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

### Manual Installation
If you prefer to install packages individually:
```bash
pip install pandas matplotlib seaborn openpyxl colorama tabulate python-dateutil pydantic pyyaml
```

## 📖 Usage

### Main Menu Options
1. **Expenses Management**
   - Add new expenses
   - List all expenses
   - Edit existing expenses
   - Delete expenses

2. **Balance Management**
   - Update bank/cash balances
   - View balance history

3. **Reports & Analysis**
   - View total expenses
   - Category summary
   - Find highest expense
   - Budget alerts
   - Export to Excel/CSV

4. **Settings & Tools**
   - Add custom categories
   - Clear memory
   - Reload categories
   - Reset to default categories

### Adding an Expense
1. Select "Expenses Management" → "Add Expense"
2. Enter amount, description, category, and payment method
3. Choose current date or enter custom date
4. Expense is automatically saved

### Exporting Data
1. Go to "Reports & Analysis" → "Export to Excel"
2. Choose export type:
   - Current month
   - Specific month
   - Custom date range
3. Files are saved to `~/Downloads/Expense Reports/`

## 📁 File Structure

```
Personal Expense Tracker/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── categories.dat         # Category data (auto-generated)
├── current_expenses.dat   # Current expenses (auto-generated)
├── expense_memory.dat     # Recent expenses (auto-generated)
└── balance_history.dat    # Balance history (auto-generated)
```

## 🔧 Configuration

### Default Categories
- Food & Groceries
- Transport
- Utilities
- Entertainment
- Shopping
- Housing
- Investment
- Healthcare
- Education
- Banking
- Miscellaneous

### Payment Methods
- Cash
- UPI
- Card

### Data Files
- **categories.dat** - Custom category names
- **current_expenses.dat** - Main expense database
- **expense_memory.dat** - Recent expenses (last 500)
- **balance_history.dat** - Bank and cash balance history

## 📊 Features in Detail

### Expense Management
- **Maximum Expenses**: 100 entries
- **Description Length**: 50 characters
- **Categories**: Up to 11 custom categories
- **Payment Methods**: 3 types (Cash, UPI, Card)

### Data Export
- **Format**: CSV with detailed analysis
- **Location**: `~/Downloads/Expense Reports/`
- **Content**: Detailed expenses, category totals, payment method breakdown
- **Analysis**: Highest expense, monthly totals, percentages

### Balance Tracking
- **Bank Balance**: Separate tracking with history
- **Cash Balance**: Separate tracking with history
- **History**: Last 100 balance updates
- **Timestamps**: Automatic date/time tracking

## 🛠️ Dependencies

### Required (Built-in)
- `os` - File system operations
- `pickle` - Data serialization
- `csv` - CSV file handling
- `dataclasses` - Data structures
- `typing` - Type hints
- `datetime` - Date/time handling

### Optional (Enhanced Features)
- `pandas` - Data analysis and manipulation
- `matplotlib` - Chart generation
- `seaborn` - Statistical visualizations
- `openpyxl` - Excel file export
- `colorama` - Colored terminal output
- `tabulate` - Formatted table display
- `python-dateutil` - Enhanced date parsing
- `pydantic` - Data validation
- `pyyaml` - Configuration management

## 🔒 Data Security

- **Local Storage**: All data stored locally on your machine
- **No Cloud Dependencies**: Works offline
- **File-based**: Simple, portable data format
- **Backup Friendly**: Easy to backup data files

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
- Ensure Python 3.7+ is installed
- Add Python to system PATH

**"Module not found"**
- Install dependencies: `pip install -r requirements.txt`
- Or run without optional packages (core functionality works)

**"Permission denied"**
- Run as administrator (Windows)
- Check file permissions

**Data not saving**
- Ensure write permissions in project directory
- Check available disk space

### Data Recovery
If data files are corrupted:
1. Backup existing `.dat` files
2. Delete corrupted files
3. Restart application (defaults will be created)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue with detailed description

## 🔄 Version History

- **v1.0** - Basic expense tracking
- **v1.1** - Added export functionality
- **v1.2** - Enhanced balance management
- **v1.3** - Added memory system and improved UI

---

**Happy Expense Tracking! 💰📊** 