// Função para preencher o dropdown com contas de anúncios do servidor Flask
function populateDropdown() {
    // Faz uma solicitação GET para o endpoint do Flask
    fetch('/get_ad_accounts')
        .then(response => response.json())  // Converte a resposta para JSON
        .then(data => {
            const selectElement = document.getElementById('adAccounts');
            // Limpa o dropdown antes de adicionar novas opções
            selectElement.innerHTML = '';
            // Itera sobre as contas de anúncios e cria um novo elemento 'option' para cada uma
            data.forEach(account => {
                const optionElement = document.createElement('option');
                optionElement.value = account.id;
                optionElement.textContent = account.name;
                selectElement.appendChild(optionElement);
            });
        })
        .catch(error => {
            console.error('Error fetching ad accounts:', error);
        });
}

// Função para definir o ID da conta de anúncio selecionada
function setAccountID(accountID) {
    console.log("Conta de anúncio selecionada: " + accountID);
    // Aqui você pode definir a variável global ou armazenar o valor conforme necessário
    // Por exemplo, você pode enviar este valor de volta para o servidor Flask se necessário
}

// Chama a função para preencher o dropdown ao carregar a página
document.addEventListener('DOMContentLoaded', populateDropdown);
