document.addEventListener("DOMContentLoaded", function () {
    console.log("Catálogo cargado correctamente");

    // Filtrar productos por categoría
    document.querySelectorAll(".category-card").forEach(card => {
        card.addEventListener("click", function () {
            const categoryId = this.dataset.category;
            filterProductsByCategory(categoryId);
        });
    });

    function filterProductsByCategory(categoryId) {
        document.querySelectorAll(".product-card").forEach(product => {
            product.style.display = product.dataset.category === categoryId ? "block" : "none";
        });
    }

    // Agregar productos a la orden
    document.querySelectorAll(".add-to-order").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.product;
            addToOrder(productId);
        });
    });

    function addToOrder(productId) {
        console.log("Producto agregado a la orden: " + productId);
        alert("Producto agregado al pedido.");
    }

    // Control del carrusel
    let carousel = document.querySelector("#catalogCarousel");
    if (carousel) {
        new bootstrap.Carousel(carousel, {
            interval: 3000,
            wrap: true
        });
    }
});
