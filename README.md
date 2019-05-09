# 4PJT-BlockChain
This is the BlockChain backend

# Install project
> Command with PowerShell
1. Install Python 3.7
    
    [Python link](https://www.python.org/downloads/)

2. Clone Supbank repository

    ```Bash
    git clone https://github.com/ThePyranhias/4PJT-SupBank-API.git
    ```

## In the cloned repository 
3. Install virtualenv
    
    ```PowerShell
    pip install virtualenv
    ```

3. Create virtual environment

    ```PowerShell
    virtualenv -p . venv
    ```
    >Now you should have a new directory "venv"

3. Activate environment

    ```
    .\venv\Scripts\Activate.ps1
    OR
    .\venv\Scripts\activate.bat
    ```

    OR
    
    From Environment 
    ```PowerShell
    cd \venv\Scripts
    .\Activate.ps1
    ```

4. Install Django
    
    ```PowerShell
    pip install Django
    ```

4. Install DRF

    ```PowerShell
    pip install djangorestframework
    ```

# Prepare launch
> Only if you change models

*Into root project*
1. Run migration

    ```PowerShell
    python manage.py makemigrations
    python manage.py migrate
    ```

# Launch project

2. Run Test

    If you need to run test    
    ```PowerShell
    cd .\SupBank_api\
    python manage.py test
    ```

2. Run server

    ```PowerShell
    cd .\SupBank_api\
    python manage.py runserver
    ```
