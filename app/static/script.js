const notes = JSON.parse(localStorage.getItem('todoNotes')) || [];
let token = localStorage.getItem('access_token');

function setToken(newToken) {
  token = newToken;
  localStorage.setItem('access_token', token);
}

async function request(url, method = 'GET', body = null) {
  const headers = {
    "Content-Type": "application/json"
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config = {
    method,
    headers
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(url, config);
  return await response.json();
}

async function addNoteServer(newNote) {
  const data = await request("/items/new_task", "POST", {
    text: newNote.text,
    isCompleted: newNote.isCompleted
  });
  console.log(data);
}

async function editNoteServer(id, oldText) {
  const note = notes.find(n => n.id === id);
  const data = await request("/items/update_task", "POST", {
    text: oldText,
    newText: note.text
  });
  console.log(data);
}

async function toggleCompleteServer(id) {
  const note = notes.find(n => n.id === id);
  const data = await request("/items/toggle_task", "POST", {
    text: note.text,
    isCompleted: note.isCompleted
  });
  console.log(data);
}

async function deleteNoteServer(id) {
  const note = notes.find(n => n.id === id);
  const data = await request("/items/delete_task", "POST", {
    text: note.text,
    isCompleted: note.isCompleted
  });
  console.log(data);
}

async function saveNotes() {
  localStorage.setItem('todoNotes', JSON.stringify(notes));
}

async function renderNotes() {
  const list = document.getElementById("notesList");
  list.innerHTML = "";

  notes.forEach(note => {
    const li = document.createElement("li");

    const span = document.createElement("span");
    span.textContent = note.text;

    if (note.isCompleted) {
      span.style.textDecoration = "line-through";
      span.style.color = "#888";
    }

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = note.isCompleted;
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

async function loadNotes() {
  renderNotes();
  const data = await request("/items/read_tasks");
  notes.length = 0;
  notes.push(...data.map((note, index) => ({
    id: note.id || index,
    text: note.text,
    isCompleted: note.isCompleted
  })));
  await saveNotes();
  renderNotes();
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
    await addNoteServer(newNote);
    notes.push(newNote);
    input.value = "";
    await saveNotes();
    renderNotes();
  }
}

async function toggleComplete(id) {
  const note = notes.find(n => n.id === id);
  if (note) {
    note.isCompleted = !note.isCompleted;
    await toggleCompleteServer(id);
    await saveNotes();
    renderNotes();
  }
}

async function editNote(id) {
  const oldText = notes.find(n => n.id === id).text;
  const newText = prompt("Введите новый текст:", oldText);
  if (newText && newText.trim()) {
    const note = notes.find(n => n.id === id);
    if (note) {
      note.text = newText.trim();
      await editNoteServer(id, oldText);
      await saveNotes();
      renderNotes();
    }
  }
}

async function deleteNote(id) {
  if (confirm("Вы уверены, что хотите удалить эту заметку?")) {
    await deleteNoteServer(id);
    notes.splice(notes.findIndex(n => n.id === id), 1);
    await saveNotes();
    renderNotes();
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const username = document.getElementById('login_username').value;
  const password = document.getElementById('login_password').value;

  try {
    const data = await request('/auth/token', 'POST', { username, password });
    if (data.access_token) {
      setToken(data.access_token);
      window.location.href = '/home';
    } else {
      alert(data.detail || 'Ошибка входа');
    }
  } catch (error) {
    console.error('Ошибка:', error);
    alert('Не удалось подключиться к серверу');
  }
}

async function handleRegister(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const data = await request('/users/new_user', 'POST', { username, password });
    if (data.status) {
      alert(data.status);
      window.location.href = '/login';
      toggleForms();
    } else {
      alert(data.detail || 'Ошибка регистрации');
    }
  } catch (error) {
    console.error('Ошибка:', error);
    alert('Не удалось зарегистрироваться');
  }
}

function toggleForms() {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  loginForm.style.display = loginForm.style.display === "none" ? "block" : "none";
  registerForm.style.display = registerForm.style.display === "none" ? "block" : "none";
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById("register-form").style.display = "none";
  document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
  document.getElementById('registerForm')?.addEventListener('submit', handleRegister);
});
loadNotes();