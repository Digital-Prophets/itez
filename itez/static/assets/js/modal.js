// Get DOM Elements
console.log("something");
const modal = document.querySelector("#my-modal");
const modalContent = document.querySelector(".modal-content");
const modalBtn = document.querySelector("#modal-btn");
const closeBtn = document.querySelector(".close");
const exportButton = document.querySelector(".export-button");

// Events
modalBtn.addEventListener("click", openModal);
closeBtn.addEventListener("click", closeModal);
window.addEventListener("click", outsideClick);
// exportButton.addEventListener("click", (e) => e.preventDefault());

console.log(modal, modalBtn, closeBtn);
// Open
function openModal() {
  modal.style.display = "block";
  modalContent.style.width = "30%";
}

// Close
function closeModal() {
  modal.style.display = "none";
}

// Close If Outside Click
function outsideClick(e) {
  if (e.target == modal) {
    modal.style.display = "none";
  }
}
