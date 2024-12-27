document.addEventListener("DOMContentLoaded", function () {
  const tokenList = [
    { name: "TestMeme", supply: 1000000, circulation: 100 },
    { name: "AlgoMeme", supply: 2000000, circulation: 500 },
  ];

  const tokenListElement = document.getElementById("token-list");
  const searchInput = document.getElementById("search-input");

  function renderTokens(filter = "") {
    tokenListElement.innerHTML = "";
    tokenList
      .filter((token) =>
        token.name.toLowerCase().includes(filter.toLowerCase())
      )
      .forEach((token) => {
        const li = document.createElement("li");
        li.textContent = `Token: ${token.name}, Supply: ${token.supply}, Circulation: ${token.circulation}`;
        tokenListElement.appendChild(li);
      });
  }

  searchInput.addEventListener("input", (e) => {
    renderTokens(e.target.value);
  });

  renderTokens();
});
