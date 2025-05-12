
let notes = JSON.parse(localStorage.getItem('todoNotes')) || [];

async function addNoteServer(newNote){
  fetch("/items/new_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userId: 3,
      text: newNote.text,
      isCompleted: newNote.isCompleted
    })
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Ошибка:', error));   
}
async function toggleCompleteServer(id){
  const note = notes.find(n => n.id === id);
  fetch("/items/toggle_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userId: 3,
      text: note.text,
      isCompleted: note.completed
    })
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Ошибка:', error));   
}
async function deleteNoteServer(id) {
  const note = notes.find(n => n.id === id);
  fetch("/items/delete_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userId: 1,
      text: note.text,
      isCompleted: note.isCompleted
    })
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Ошибка:', error));
} 

function saveNotes() {
  localStorage.setItem('todoNotes', JSON.stringify(notes));
}


function loadNotes() {
  renderNotes();
}

function renderNotes() {
  const list = document.getElementById("notesList");
  list.innerHTML = "";

  notes.forEach(note => {
    const li = document.createElement("li");

    const span = document.createElement("span");
    span.textContent = note.text;

    if (note.completed) {
      span.style.textDecoration = "line-through";
      span.style.color = "#888";
    }

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = note.completed;
    checkbox.onclick = () => toggleComplete(note.id);

    const actions = document.createElement("div");
    actions.className = "actions";

    const editBtn = document.createElement("button");
    editBtn.textContent = "Редактировать";
    editBtn.onclick = () => editNote(note.id);

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Удалить";
    deleteBtn.onclick = () => deleteNote(note.id);

    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(actions);

    list.appendChild(li);
  });
}


async function addNote() {
  const input = document.getElementById("newNoteInput");
  const text = input.value.trim();

  if (text !== "") {
    const newNote = {
      id: Date.now(),
      text: text,
      isCompleted: false
    };
    await addNoteServer(newNote)
    notes.push(newNote);
    input.value = "";
    saveNotes();
    renderNotes();
  }
}


async function toggleComplete(id) {
  const note = notes.find(n => n.id === id);
  if (note) {
    note.completed = !note.completed;
    await toggleCompleteServer(id)
    saveNotes();
    renderNotes();
  }
}


async function editNote(id) {
  const newText = prompt("Введите новый текст:", notes.find(n => n.id === id).text);
  if (newText !== null && newText.trim() !== "") {
    const note = notes.find(n => n.id === id);
    if (note) {
      note.text = newText.trim();
      saveNotes();
      renderNotes();
    }
  }
}


async function deleteNote(id) {
  if (confirm("Вы уверены, что хотите удалить эту заметку?")) {
    await deleteNoteServer(id);
    notes = notes.filter(n => n.id !== id);
    saveNotes();
    renderNotes();
  }
}

loadNotes();

function toggleForms() {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");

  if (loginForm.style.display === "none") {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
  } else {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
  }
}
document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch('/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': '{{ csrf_token }}' 
            },
            body: JSON.stringify({
                username: formData.get('username'),
                password: formData.get('password')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                localStorage.setItem('access_token', data.access_token);
                window.location.href = '/'; 
            } else {
                alert(data.detail);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('registerForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch('/users/new_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': '{{ csrf_token }}' 
            },
            body: JSON.stringify({
                username: formData.get('username'),
                password: formData.get('password')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                
                window.location.href = '/login'; 
            } else {
                alert(data.status);
            }
        })
        .catch(error => console.error('Error:', error));
    });