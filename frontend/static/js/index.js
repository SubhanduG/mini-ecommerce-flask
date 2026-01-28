document.addEventListener("DOMContentLoaded", () => {
  checkLoginStatus();
  loadProducts();
});

let isLoggedIn = false;

function checkLoginStatus() {
  fetch("/auth/me", { credentials: "include" })
    .then(res => res.json())
    .then(data => {
      isLoggedIn = data.logged_in === true;

      const userActions = document.getElementById("userActions");
      const authButtons = document.getElementById("authButtons");

      if (isLoggedIn) {
        authButtons.classList.add("d-none");
        userActions.classList.remove("d-none");
        updateCartCount();
      } else {
        authButtons.classList.remove("d-none");
        userActions.classList.add("d-none");
        document.getElementById("cartCount").innerText = 0;
      }
    })
    .catch(err => console.error("Error checking login status:", err));
}

function loadProducts() {
  fetch("/products", { credentials: "include" })
    .then(res => res.json())
    .then(products => {
      const list = document.getElementById("productList");
      list.innerHTML = "";

      products.forEach(p => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";
        card.innerHTML = `
          <div class="card shadow">
              <img src="${p.image}" class="card-img-top" alt="${p.name}" style="height:200px; object-fit:contain; width:100%; background-color:#f8f9fa;">
              <div class="card-body">
                  <h5>${p.name}</h5>
                  <p>Price: $${p.price}</p>
                  <p>Stock: ${p.stock}</p>
                  <button class="btn btn-primary btn-sm">Add to Cart</button>
              </div>
          </div>
        `;
        const btn = card.querySelector("button");
        btn.addEventListener("click", () => handleLoginRequired(() => addToCart(p.id)));
        list.appendChild(card);
      });
    })
    .catch(err => console.error("Error loading products:", err));
}

function handleLoginRequired(action) {
  if (!isLoggedIn) {
    if (confirm("Login required to perform this action. Go to login page?")) {
      window.location.href = "/login";
    }
    return;
  }
  action();
}

function addToCart(productId) {
  fetch("/cart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Product added to cart");
        updateCartCount();
      }
    })
    .catch(err => console.error("Error adding to cart:", err));
}

function updateCartCount() {
  fetch("/cart/count", { credentials: "include" })
    .then(res => res.json())
    .then(data => {
      document.getElementById("cartCount").innerText = data.count || 0;
    })
    .catch(err => console.error("Error fetching cart count:", err));
}

function goToCart() {
  handleLoginRequired(() => window.location.href = "/order-summary");
}

function placeOrder() {
  handleLoginRequired(() => {
    fetch("/orders/confirm", {
      method: "POST",
      credentials: "include",
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          alert("Order placed successfully!");
          updateCartCount();
          window.location.href = "/order-summary";
        }
      })
      .catch(err => console.error("Error placing order:", err));
  });
}

function logout() {
  fetch("/auth/logout", { method: "POST", credentials: "include" })
    .then(res => res.json())
    .then(() => {
      const userActions = document.getElementById("userActions");
      const authButtons = document.getElementById("authButtons");

      authButtons.classList.remove("d-none");
      userActions.classList.add("d-none");

      isLoggedIn = false;
      document.getElementById("cartCount").innerText = 0;
      window.location.href = "/";
    })
    .catch(err => console.error("Error logging out:", err));
}