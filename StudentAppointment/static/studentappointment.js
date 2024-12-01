function filterSlots(selectedDate) {
  const slots = document.querySelectorAll('.timeselection');
  const showForm = document.querySelector('.show');
  const dates = new Set(); // create a Set to store unique dates

  // loop through slots to hide/show based on selected date
  for (let i = 0; i < slots.length; i++) {
    const slot = slots[i];
    const slotDate = slot.dataset.date;
    if (slotDate === selectedDate) {
      slot.style.display = 'block';
    } else {
      slot.style.display = 'none';
    }
    // add unique date to the Set
    dates.add(slotDate);
  }

  // loop through dropdown options to show/hide based on unique dates
  const dropdownOptions = document.querySelectorAll('.dropdowndates option');
  for (let i = 0; i < dropdownOptions.length; i++) {
    const option = dropdownOptions[i];
    const optionValue = option.value;
    if (optionValue === "--") {
      option.style.display = 'block';
    } else if (dates.has(optionValue)) {
      option.style.display = 'block';
      dates.delete(optionValue); // remove date from Set to prevent duplicates
    } else {
      option.style.display = 'none';
    }
  }

  // show or hide time container based on selected date
  const timeContainer = document.querySelector('.timeContainer');
  if (selectedDate === '--') {
    timeContainer.style.display = 'none';
  } else {
    timeContainer.style.display = 'inline-flex';
  }

  // hide form until both date and time are selected
  showForm.style.display = 'none';

  // uncheck radio button if one is selected
  const selectedRadio = document.querySelector('input[name="time"]:checked');
  if (selectedRadio) {
    selectedRadio.checked = false;
  }
}

function selectTime(selectedTime) {
  const showForm = document.querySelector('.show');

  // show form when a time is selected
  showForm.style.display = 'block';
}

window.onload = function() {
  filterSlots('--');
};

const dateDropdown = document.getElementById("dateDropdown");
const inputFields = document.querySelectorAll(".inputBoxtitle input");

dateDropdown.addEventListener("change", () => {
  // Get the selected date
  const selectedDate = dateDropdown.value;

  // Clear the input fields if the selected date changes
  inputFields.forEach((input) => {
    if (input.value && input.dataset.date !== selectedDate) {
      input.value = "";
    }
  });
});
