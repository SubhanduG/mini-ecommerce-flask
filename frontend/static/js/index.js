const BASE_URL = "http://127.0.0.1:5000";

fetch(`${BASE_URL}/products`)
  .then(res => res.json())
  .then(products => {
    const list = document.getElementById("productList");

    products.forEach(p => {
      list.innerHTML += `
        <div class="col-md-4 mb-3">
          <div class="card shadow">
            <div class="card-body">
              <h5>${p.name}</h5>
              <p>Price: $${p.price}</p>
              <p>Stock: ${p.stock}</p>
              <button class="btn btn-primary btn-sm"
                      onclick="addToCart(${p.id})">
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      `;
    });
  })
  .catch(err => console.error("Error loading products:", err));

function showCartActions() {
  document.getElementById("cartActions").classList.add("show");
}

function hideCartActions() {
  document.getElementById("cartActions").classList.remove("show");
}

function goToOrderSummary() {
  window.location.href = "/order-summary";
}

function placeOrderFromHover(event) {
  event.stopPropagation();
  window.location.href = "/order-summary";
}

function updateCartCount() {
  fetch(`${BASE_URL}/cart/count`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("cartCount").innerText = data.count || 0;
    })
    .catch(() => {
      document.getElementById("cartCount").innerText = 0;
    });
}

document.addEventListener("DOMContentLoaded", updateCartCount);

function addToCart(productId) {
  fetch(`${BASE_URL}/cart`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  })
    .then(res => res.json())
    .then(() => {
      updateCartCount();
      alert("Product added to cart");
    })
    .catch(err => console.error("Add to cart error:", err));
}

