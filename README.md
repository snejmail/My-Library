# My-Library 📚
Create your own reading lists and add books to them, browsing from a large books database.

## Features   
 - User authentication: Register and log in securely.  
 - Explore a database of books available in the library.  
 - Create custom reading lists to organize favorite books.  
 - Add and remove books from your personalized lists.  

## Technologies Used  
 - Backend: Django (Python)  
 - Frontend: HTML, CSS, JavaScript  
 - Database: PostgreSQL  
 - File Upload: Django's File Handling and Media Features  

## Project Setup
- **Clone the repo:**  
    ```bash
    git clone https://github.com/snejmail/My-Library  
    cd My-Library  
    ```

- **Set up a virtual environment and activate it:**  
    ```bash
    python -m venv venv  
    venv\Scripts\activate  
    ```

- **Install dependencies:**  
    ```bash
    pip install -r requirements.txt  
    ```

- **Change DB settings in `settings.py`:**  
    ```python
    DATABASES = {  
        "default": {  
            "ENGINE": "django.db.backends.postgresql",  
            "NAME": "your_db_name",  
            "USER": "your_username",  
            "PASSWORD": "your_pass",  
            "HOST": "127.0.0.1",  
            "PORT": "5432",  
        }  
    }  
    ```

- **Apply database migrations:**  
    ```bash
    python manage.py migrate  
    ```

- **Create a superuser:**  
    ```bash
    python manage.py createsuperuser  
    ```

- **Run the project:**  
    ```bash
    python manage.py runserver  
    ```

- **Visit the app at http://127.0.0.1:8000/.**  


## Usage
- **Register/Login:** Create an account or log in to start uploading.  
- **Explore the Library** Browse the collection of books available in the library.  
- **Creating Reading Lists** Create your custom reading lists and organize your books by adding and removing them from the lists.  


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
