# The Chatter Box

The Chatter Box is a web application where like-minded people can connect through rooms to share their problems and thoughts. Users can join existing rooms or create custom rooms for specific discussions.

---

## Features

- **Join Rooms:** Enter existing rooms by simply messaging within them.  
- **Create Custom Rooms:** Personalize your discussions by creating new rooms.  
- **User-Friendly Interface:** Easy navigation and interaction.  

---

## Installation

Follow these steps to set up the project on your local machine:

```markdown
1. **Clone the Repository:**
        git clone https://github.com/Param00Developer/ChatterBox.git
   Then :
        cd ChatterBox
```
Create a Virtual Environment:

```markdown
2. python -m venv venv
```

Activate the Virtual Environment:
```markdown
3. For Windows:
      venv\Scripts\activate
   For macOS/Linux:
      source venv/bin/activate
```

Install Required Dependencies:

```markdown
4. pip install -r requirements.txt
```

Run Migrations:
```markdown
5. python manage.py migrate
```
Start the Development Server:
```markdown
6. python manage.py runserver
```
Access the Application:
```markdown
7. Open your browser and navigate to http://127.0.0.1:8000/
```

---

## Requirements

Add the following dependencies to `requirements.txt` if they are not already present:

```markdown
-Django==5.1.1
-djangorestframework==3.15.2
-pip==24.2 
```
## Usage
1. Access the App: After installation, run the application using ``python manage.py runserver`` and navigate to ``http://127.0.0.1:8000/`` in your web browser.  
2. Join an existing room or create a custom room . 
3. Simply message the room you're interested in to gain access.
4. Start chatting and sharing your thoughts with others!

---
## Contributing
 We Welcome Your Contributions!
```markdown
1. Fork the Project
2. Create Your Feature Branch: git checkout -b feature/NewIdea
3. Commit Your Changes: git commit -m 'Add NewIdea'
4. Push to the Branch: git push origin feature/NewIdea
5. Open a Pull Request
```
## Contact
For any questions or suggestions, feel free to reach out:

```markdown
**GitHub:** [Param00Developer](https://github.com/Param00Developer)
```
