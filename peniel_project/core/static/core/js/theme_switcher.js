document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('theme-toggle-dark-icon');
    const lightIcon = document.getElementById('theme-toggle-light-icon');

    // --- CONFIGURAÇÃO DO DESENVOLVEDOR ---
    // Altere estas constantes para definir qual tema de cores será usado para os modos claro e escuro.
    // Os nomes devem corresponder aos atributos `data-theme` no seu arquivo `themes.css`.
    // Use 'default' para usar o tema padrão definido no seletor `:root` do CSS.
    const DEVELOPER_CHOICE_LIGHT_THEME = 'default'; // Opções: 'default', 'azul', 'verde', 'roxo', 'amarelo', 'pb', 'ciano', 'rosa', 'vermelho'
    const DEVELOPER_CHOICE_DARK_THEME = 'default';  // Opções: 'default', 'azul', 'verde', 'roxo', 'amarelo', 'pb', 'ciano', 'rosa', 'vermelho'

    /**
     * OPÇÕES DE ARMAZENAMENTO DA PREFERÊNCIA DO TEMA:
     * 
     * 1. localStorage (ESCOLHIDO PARA ESTE EXEMPLO):
     *    - O que é: Armazenamento persistente no navegador. Os dados não expiram.
     *    - Vantagem: A escolha do tema do usuário é lembrada entre as sessões. Se ele fechar e abrir o navegador, o tema escolhido será mantido.
     *    - Desvantagem: Os dados ficam no navegador até serem limpos manualmente.
     * 
     * 2. sessionStorage:
     *    - O que é: Armazenamento temporário. Os dados são limpos quando a aba/janela do navegador é fechada.
     *    - Vantagem: Útil se você quer que o tema reset para o padrão a cada nova visita.
     *    - Desvantagem: O usuário precisa escolher o tema toda vez que abre o site.
     *    - Como usar: Troque `localStorage` por `sessionStorage` em todo o código.
     * 
     * 3. Banco de Dados (via API):
     *    - O que é: Salvar a preferência no perfil do usuário no seu banco de dados.
     *    - Vantagem: A preferência é sincronizada entre diferentes dispositivos e navegadores. Se o usuário logar em outro computador, o tema dele será carregado. É a solução mais robusta.
     *    - Desvantagem: Requer mais implementação (criar um campo no modelo `Usuario`, uma URL e uma view para receber a atualização via `fetch`).
     *    - Como usar: No clique do botão, em vez de salvar no localStorage, você faria uma requisição `fetch` para uma view no Django, enviando o novo tema. Ao carregar a página, o Django já renderizaria o HTML com o atributo `data-mode` correto.
     */

    // Função para aplicar o tema e atualizar o ícone
    const applyTheme = (themeMode) => {
        if (themeMode === 'escuro') {
            document.documentElement.setAttribute('data-mode', 'escuro');
            // Aplica o tema escuro específico escolhido pelo desenvolvedor
            document.documentElement.setAttribute('data-theme', DEVELOPER_CHOICE_DARK_THEME);
            darkIcon.classList.add('d-none');
            lightIcon.classList.remove('d-none');
        } else {
            document.documentElement.setAttribute('data-mode', 'claro');
            // Aplica o tema claro específico escolhido pelo desenvolvedor
            document.documentElement.setAttribute('data-theme', DEVELOPER_CHOICE_LIGHT_THEME);
            darkIcon.classList.remove('d-none');
            lightIcon.classList.add('d-none');
        }
    };

    // Verifica a preferência salva no localStorage
    const storedTheme = localStorage.getItem('theme');

    // Verifica a preferência do sistema operacional do usuário
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Define o tema inicial: 1º localStorage, 2º preferência do SO, 3º padrão (claro)
    const initialTheme = storedTheme ? storedTheme : (prefersDark ? 'escuro' : 'claro');
    applyTheme(initialTheme);

    // Adiciona o evento de clique ao botão
    themeToggleBtn.addEventListener('click', () => {
        // Verifica qual é o tema atual e define o novo tema
        const currentMode = document.documentElement.getAttribute('data-mode');
        const newTheme = currentMode === 'claro' ? 'escuro' : 'claro';

        // Aplica o novo tema
        applyTheme(newTheme);

        // Salva a nova preferência no localStorage
        localStorage.setItem('theme', newTheme);
    });
});
