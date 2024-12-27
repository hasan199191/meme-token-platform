# README.md

# Algorand Meme Platform

The Algorand Meme Platform is a decentralized application that allows users to create, trade, and manage meme tokens on the Algorand blockchain. This project consists of smart contracts, a backend API, and a frontend interface.

## Project Structure

- **smart_contracts/**: Contains the smart contracts for the meme token and trading operations.
  - `meme_token.py`: Implementation of the token contract.
  - `trading.py`: Implementation of trading operations.

- **backend/**: The backend API that handles requests and integrates with the Algorand blockchain.
  - **api/**: Contains the API routes and request handlers.
    - `routes.py`: Defines the API routes.
    - `handlers.py`: Contains request handlers for the API.
  - **services/**: Contains services for blockchain integration and token management.
    - `algorand.py`: Handles integration with the Algorand blockchain.
    - `wallet.py`: Manages integration with PeraWallet.
    - `token.py`: Manages token-related operations.
  - **models/**: Defines the data schema for the backend application.
    - `schema.py`: Contains the data schema definitions.

- **frontend/**: The user interface for the application.
  - **templates/**: Contains HTML templates for the frontend.
    - `base.html`: Base template for the application.
    - `home.html`: Home page template.
    - `trading.html`: Trading page template.
  - **static/**: Contains static files such as CSS, JavaScript, and images.

- **tests/**: Contains unit tests for the application.
  - `test_contracts.py`: Unit tests for the smart contracts.
  - `test_services.py`: Unit tests for the backend services.

- **config/**: Contains configuration settings for the application.
  - `settings.py`: Configuration settings.

- **requirements.txt**: Lists the dependencies required for the project.

- **main.py**: Entry point of the application, initializing and running the server.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd algorand-meme-platform
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.