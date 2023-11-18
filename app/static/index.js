function toggleDropdown(element) {
    element.classList.toggle("active");
}

document.addEventListener('DOMContentLoaded', function () {
    const options = document.querySelectorAll('.option');
  
    options.forEach(option => {
      option.addEventListener('click', function () {
        // Remove 'active' class from all options
        options.forEach(opt => opt.classList.remove('active'));
  
        // Add 'active' class to the clicked option
        this.classList.add('active');
      });
    });
  });
  
  document.addEventListener('DOMContentLoaded', function () {
    const researchFrame = document.querySelector('.research-frame');
  
    researchFrame.addEventListener('click', function () {
      researchFrame.classList.toggle('expanded');
    });
  });
  function slideCard(card) {
    // Hide all cards
    document.querySelectorAll('.team-card').forEach(function (c) {
      c.style.display = 'none';
    });
  
    // Create a new card element
    const newCard = card.cloneNode(true);
  
    // Append the new card to the container
    card.parentNode.appendChild(newCard);
  
    // Show the original card
    card.style.display = '';
  
    // Slide the original card to the left
    card.style.transform = 'translateX(-100%) scale(0.8)'; // Adjust the scale value as needed
  
    // Enlarge the new card at the right side
    newCard.style.transform = 'scale(2) translateX(25%) translateY(-20%)'; // Adjust the scale value as needed
    newCard.style.display = 'flex'; // Make sure the new card is displayed
  
    // You may want to hide overflow on the new card if it contains long text
    newCard.querySelector('.card-body').style.overflow = 'auto';
  
    // Optionally, you can also adjust the font size of the new card
    newCard.querySelectorAll('.card-title, .card-text').forEach(function (element) {
      element.style.fontSize = '1em'; // Adjust the font size as needed
    });
  }
  