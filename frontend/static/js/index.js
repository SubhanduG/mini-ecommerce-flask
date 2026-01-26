const API_URL = "http://127.0.0.1:5000/products";

fetch(API_URL).then(response => response.json()).then(data => {
  const list = document.getElementById("productList");
  data.forEach(p => {
    list.innerHTML += `
        <div class="col-md-4 mb-3">
          <div class="card shadow">
            <div class="card-body">
              <h5>${p.name}</h5>
              <p>${p.price}</p>
              <p>${p.stock}</p>
              <button class="btn btn-primary btn-sm">Add to Cart</button>
            </div?
          </div?
        </div>      
        `;

  });
});