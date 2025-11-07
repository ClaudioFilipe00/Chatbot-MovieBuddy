const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// URL base do seu servidor FastAPI
const API_URL = "http://127.0.0.1:8000";

// --- Função Auxiliar: Adiciona uma Mensagem ao Chat ---
function appendMessage(text, sender) {
    // Substitui **texto** por <strong>texto</strong> para formatação visual (Markdown)
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.innerHTML = formattedText; // Usa innerHTML para renderizar o <strong>
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// --- Funções Auxiliares de Filmes ---
function showPopup(filme) {
    const popup = document.createElement("div");
    popup.classList.add("popup");
    popup.innerHTML = `
        <div class="popup-content" style="background-image: url('${filme.poster}')">
            <button class="close-btn">×</button>
            <div class="popup-info">
                <h2>${filme.titulo}</h2>
                <p><span class="nota">⭐ ${filme.nota.toFixed(1)}</span></p>
                <p>${filme.sinopse}</p>
            </div>
        </div>
    `;

    document.body.appendChild(popup);

    popup.querySelector(".close-btn").addEventListener("click", () => {
        popup.remove();
    });
}

function appendFilmes(filmes) {
    const grid = document.createElement("div");
    grid.classList.add("filmes-grid");

    filmes.forEach(f => {
        const card = document.createElement("div");
        card.classList.add("card");
        
        card.innerHTML = `<img src="${f.poster || ''}" alt="${f.titulo}">`;

        card.addEventListener("click", () => showPopup(f));
        grid.appendChild(card);
    });

    chatBox.appendChild(grid);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// --- Função Principal: Enviar Mensagem para o Chatbot ---
async function sendMessage() {
    const text = userInput.value.trim();
    
    const isInitialCall = chatBox.children.length === 0;
    const mensagem_enviada = isInitialCall ? 'iniciar' : text;
    
    if (!text && !isInitialCall) return;

    if (text) {
        appendMessage(text, "user");
    }
    userInput.value = "";

    appendMessage("Digitando...", "bot");

    try {
        userInput.disabled = true;
        sendBtn.disabled = true;

        const res = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: mensagem_enviada })
        });
        const data = await res.json();

        // 3. Remove o "Digitando..."
        const last = chatBox.querySelector(".bot:last-child");
        if (last) chatBox.removeChild(last);

        // 4. Adiciona a resposta do bot (texto)
        if (data.resposta) {
            appendMessage(data.resposta, "bot");
        } 

        // 5. Adiciona a grade de filmes, se houver
        if (data.filmes && data.filmes.length > 0) {
            appendFilmes(data.filmes);
        }

    } catch (err) {
        // 3. Remove o "Digitando..." e mostra o erro
        const last = chatBox.querySelector(".bot:last-child");
        if (last) chatBox.removeChild(last);
        appendMessage("Erro: Não foi possível conectar ao servidor. Verifique se o FastAPI está rodando.", "bot");
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// --- Função para Carregar a Mensagem Inicial (Chama sendMessage com lógica de 'iniciar') ---
function loadInitialMessage() {
    // Apenas faz a primeira chamada se o chat estiver vazio
    if (chatBox.children.length === 0) {
        sendMessage(); 
    }
}


// --- Event Listeners ---
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", e => e.key === "Enter" && sendMessage());


// --- CHAMA A MENSAGEM INICIAL AO CARREGAR A PÁGINA ---
document.addEventListener("DOMContentLoaded", loadInitialMessage);