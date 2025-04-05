document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".add-to-cart");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      alert("Item added to cart!");
    });
  });
});
