# Django Social Media App

## **Description**

The Django Social Media App is a feature-rich social media platform developed with Django. It provides users with an engaging experience through profile management, post creation, commenting, liking, and following other users. The app includes a feed that aggregates posts from users in the network, allowing for seamless content consumption and interaction.

## **Features**

- **User Authentication:** Sign up, log in, and log out.
- **User Profiles:** Manage and view user profiles.
- **Post Creation:** Create, view, and delete posts.
- **Comments:** Add and view comments on posts.
- **Likes:** Like and unlike posts.
- **Image Uploads:** Upload and display images with posts.
- **Feed:** A dynamic feed that displays posts from users you follow.
- **Follow/Unfollow:** Follow and unfollow other users.
- **Responsive Design:** Optimized for various devices and screen sizes.

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Abdlruhmann/Django_Social_Media_App.git

    Navigate to the project directory:

bash

    cd Django_Social_Media_App

    Create and activate a virtual environment:

bash

    python -m venv env
    source env/bin/activate   # On Windows use: .\env\Scripts\activate

    Install the required packages:

bash

    pip install -r requirements.txt

    Apply migrations:

bash

    python manage.py migrate

    Create a superuser (optional but recommended for admin access):

bash

    python manage.py createsuperuser

    Run the development server:

bash

    python manage.py runserver

    Open your browser and go to:

arduino

    http://127.0.0.1:8000/

Usage

    User Registration: Sign up to create an account.
    Login: Log in with your credentials.
    Feed: View the dynamic feed to see recent posts from users you follow.
    Create Posts: Share your thoughts and media.
    Interact: Like, comment, and follow users.
    Manage Profile: Update your profile information and view your posts.

Contributing

    Fork the repository.

    Create a new branch for your feature or fix:

    bash

        git checkout -b feature/your-feature-name

        Commit your changes:

bash

git commit -am 'Add new feature or fix'

Push the branch to your fork:

bash

    git push origin feature/your-feature-name

    Create a pull request on GitHub.

Acknowledgements

    Django for providing the framework
    Bootstrap for styling and responsiveness
    [Other libraries or resources used]