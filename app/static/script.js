
let notes = JSON.parse(localStorage.getItem('todoNotes')) || [];

async function addNoteServer(newNote) {
  fetch("/items/new_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userID: 14,
      text: newNote.text,
      isCompleted: newNote.isCompleted
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Ошибка:', error));
}
async function editNoteServer(id, text) {
  const note = notes.find(n => n.id === id);
  fetch("/items/update_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userID: 14,
      text: note.text,
      isCompleted: note.isCompleted,
      newText: text
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Ошибка:', error));
}
async function toggleCompleteServer(id) {
  const note = notes.find(n => n.id === id);
  fetch("/items/toggle_task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      userID: 14,
      text: note.text,
      isCompleted: note.isCompleted
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
      userID: 14,
      text: note.text,
      isCompleted: note.isCompleted
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Ошибка:', error));
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
async function loadNotes() {
  try {
    const response = await fetch("/items/read_tasks?userID=14");
    const data = await response.json();

    notes = data.map((note, index) => ({
      id: note.id || index,
      text: note.text,
      isCompleted: note.isCompleted
    }));
    saveNotes();
  }
  catch (error) {
    console.error("Ошибка загрузки заметок:", error);
  }
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
      await editNoteServer(id, newText)
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

async function toggleForms() {
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
