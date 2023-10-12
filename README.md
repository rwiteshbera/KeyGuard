# KeyGuard: A Local Password Manager

KeyGuard is a simple and secure password manager that allows you to store and retrieve your passwords and other sensitive information locally on your computer. This password manager is designed to be easy to use and provides a safe and convenient way to manage your passwords. Here, we will guide you through the usage of KeyGuard.

![CLI](/assets/cli.png)

## Getting Started

### Installation

Before using KeyGuard, make sure you have Python (latest) installed on your system. You can download Python from [python.org](https://www.python.org/downloads/). Follow these steps to get started:

1. Clone the KeyGuard repository from GitHub:
   ```
   git clone https://github.com/rwiteshbera/KeyGuard.git
   cd KeyGuard
   ```

2. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. Run KeyGuard using the following command:
   ```
   python main.py
   ```

## Security Flowchart

For a visual representation of the KeyGuard security flow, please refer to our Figma flowchart:

[Figma KeyGuard Flowchart](https://shorturl.at/mCN58)

![KeyGuard Flowchart](/assets/keyguard.png)

## Command Line Usage

KeyGuard provides a command-line interface for managing your passwords and vault. Here are the available commands:

### Initialize the Vault

To set up your KeyGuard vault for the first time, run the following command:

```shell
python main.py --init
```

You will be prompted to create a vault by providing a **vault name** and a **master password**. Make sure to choose a strong master password as it is used to encrypt and decrypt your vault. Keep this master password in a safe place.

### Add a New Entry

To add a new entry to your KeyGuard vault, use the following command:

```shell
python main.py --add
```

You will be asked to log in by providing your **master password**. This password is required to access your vault.

### Retrieve an Entry

To retrieve an entry from your KeyGuard vault, run the following command:

```shell
python main.py --get
```

You will again be asked to log in with your **master password**.

### Help Section
You can access the help section for KeyGuard's command-line interface by running:

```shell
python main.py --help
```

This will display detailed information about each available command and their respective options.

## Contact

If you have any questions, suggestions, or encounter any issues, please don't hesitate to [create an issue](https://github.com/rwiteshbera/KeyGuard/issues) on our GitHub repository. We appreciate your feedback and are here to assist you.