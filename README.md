# SubletScript

A CLI tool designed for tenants to track monthly utility bills and rent payments. It stores data in a local JSON file, allowing users to log expenses, categorize them (water, electric, internet, rent), and generate a formatted summary report in the terminal. It includes features to compare current monthly spending against a predefined budget and alerts the user if they are overspending for the month, helping individuals manage their living costs without complex accounting software.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Future Work](#future-work)
- [License](#license)

## Installation

```bash
git clone <repo-url>
cd subletscript
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Run the main entry point to start SubletScript.

## Project Structure

```
├── cli.py
├── models.py
├── storage.py
├── analytics.py
├── utils.py
├── requirements.txt
└── README.md
```

## Modules

- **entry_point**: Core module for entry_point functionality.
- **core**: Core module for core functionality.
- **persistence**: Core module for persistence functionality.
- **utils**: Core module for utils functionality.

## Future Work

- [ ] Add comprehensive test suite
- [ ] Implement CI/CD pipeline
- [ ] Add Docker support
- [ ] Improve error handling and edge cases
- [ ] Add configuration documentation
- [ ] Performance optimization

## License

This project is licensed under the MIT License.
