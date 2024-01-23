import streamlit as st
import requests
BASE_URL = "http://127.0.0.1:8000"
col1 ,col2 ,col3=st.columns(3)
with st.container():
    col1.title("Todo App")
    col2.write("")
    col3.write(" ")
    col3.write(" ")
    if 'loggedin'in st.session_state:
        if st.session_state['loggedin']: 
            if col3.button("Logout"):
                st.session_state['loggedin'] = False
                st.rerun()
header_section = st.container()
login_section = st.container()
signup_section = st.container()

def loggedin_pressed(email ,password):
    response = requests.post(f'http://127.0.0.1:8000/login', json={"email": email, "password": password})
    if response.status_code == 200:
        st.success("Login successful!")
        st.session_state['loggedin'] = True
        st.session_state['user'] = response.json()
    else:
        st.session_state['loggedin'] = False
        st.error("Invalid username or password")

def show_login_page():
    with login_section:
        if st.session_state['loggedin'] == False:
            st.title("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            st.button("Login" , on_click =loggedin_pressed ,args=(email ,password))

def signup_clicked(name , email , password ,confirm_password):
    if password == confirm_password:
        response = requests.post(f'http://127.0.0.1:8000/signup', json={"name": name, "email": email, "password": password})
        if response.status_code == 200:
            st.success("Signup successful!")
            st.session_state['loggedin'] = True
            
    else:
        st.error("Signup failed")

def signup():
    with signup_section:
        st.title("Signup")
        name = st.text_input("Name")
        email = st.text_input("Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Signup",on_click=signup_clicked ,args=(name , email , new_password ,confirm_password)):
            st.rerun()
            
                
            

def delete_todo(id):
    res = requests.delete(f"http://127.0.0.1:8000/todos/{id}")
    if res.status_code == 200:
        st.success("Todo deleted successfully")
        #st.rerun()
    else:
        st.error(f"Error deleting todo  {id}")
        
def updatetodo(user ,name , descrpt):
    r = requests.put(f"http://127.0.0.1:8000/todos/{state.edit_todo_id}", json={"name": name, "description": descrpt, "uid": user})
    if r.status_code == 200:
        st.success("Todo updated successfully")
    else:
        st.error("Error updating todo")       


class SessionState:
    def __init__(self):
        self.edit_mode = False
        self.edit_todo_id : int = None

state = SessionState()


def show_home_page(user: str):
    new_todo = st.text_input("Add new todo:")
    description = st.text_input("Description:")
    
    if st.button("Add Todo"):
        r = requests.post("http://127.0.0.1:8000/post/todo", json={"name": new_todo, "description": description, "uid": user})
        st.success(f"Todo added: {new_todo}")
        st.rerun()

    response = requests.get(f"http://127.0.0.1:8000/show_todos?uid={user}")
    if response.status_code == 200:
        todos = response.json()
        if not todos:
            st.header("No todos found.")
        else:
            i = 0
            c1, c2, c3, c4 = st.columns(4)
            c1.write("Todo Name")
            c2.write("Description")
            c3.write(" ")
            c4.write(" ")
            c3.write(" ")
            c4.write(" ")
            st.text("________________________________________________________________________")
            for todo in todos:
                with st.container():
                    c1.write(f"{todo['name']} ")
                    c2.write(f"{todo['description']}")
                    
                    if c3.button("Delete", on_click=delete_todo, args=(todo['todo_id'],), key=todo['todo_id']):
                        pass  # Do nothing, as delete_todo will handle it
                    
                    if c4.button("Edit", key=i):
                        # Set the edit mode and todo_id in the session state
                        state.edit_mode = True
                        state.edit_todo_id = todo['todo_id'] 
                        
                i += 1

            # Sidebar for editing
            if state.edit_mode:
                with st.sidebar:
                    name = st.text_input(f"Edit Name {state.edit_todo_id}")
                    descrpt = st.text_input("Edit Description")
                    if st.button("Save Changes" , on_click=updatetodo ,args=(user ,name , descrpt)):
                        st.rerun()
                        
    else:
        st.error(f"Error fetching todos. Status code: {response.status_code}")



with header_section :
    

    if 'loggedin' not in st.session_state:
        st.session_state['user'] = None
        st.session_state['loggedin'] = False
        if st.session_state['loggedin']:
            show_home_page(st.session_state['user'])
        else:
            st.title("Login or Signup")
            on = st.toggle(f"Login / Signup")
            if on:
                signup()
            else:
                show_login_page()

    else:
        if st.session_state['loggedin']:
            show_home_page(st.session_state['user'])
        else:
            st.title("Login or Signup")
            on = st.toggle(f"Login / Signup")
            if on:
                signup()
            else:
                show_login_page()



