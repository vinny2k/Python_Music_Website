"""
code adapted from tutorial
TechnoDine, Create a dynamic website with python - python from scratch - creating website with Flask- Lesson 36. 2020. 
https://www.youtube.com/watch?v=5Wx7U58SKhg&ab_channel=TechnoDine
"""
from app import create_app

app = create_app()

if __name__=="__main__":
    app.run(debug=True)