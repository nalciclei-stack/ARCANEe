document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.boxShadow = "0 0 25px #00FFB2";
        });

        card.addEventListener("mouseleave", () => {
            card.style.boxShadow = "none";
        });
    });
});