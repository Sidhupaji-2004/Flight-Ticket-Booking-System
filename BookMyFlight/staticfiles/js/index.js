
/* The code snippet you provided is adding event listeners to various elements on the page when the DOM
content has finished loading. Here's a breakdown of what each part of the code is doing: */
console.log('script has loaded.');
document.addEventListener("DOMContentLoaded", () => {
    document.querySelector('#flight-from').addEventListener("input", event => {
        flight_from(event);
    })

    document.querySelector('#flight-to').addEventListener("input", event => {
        flight_to(event);
    })

    document.querySelector('#flight-from').addEventListener("focus", event => {
        flight_from(event);
    })

    document.querySelector('#flight-to').addEventListener("focus", event => {
        flight_to(event);
    })

    document.querySelectorAll('.trip-type').forEach(type => {
        type.onClick = trip_type;
    })


})

function flight_from(event, focus = false) {
    let input = event.target;
    let list = document.querySelectorAll('#places_from');
    showplaces(input);

    if (!focus) {
        input.dataset.value = "";
    }

    if (input.value.length > 0) {
        fetch('query/places/' + input.value)
            .then(response => response.json())
            .then(places => {
                list.innerHTML = '';
                places.forEach(place => {
                    let div = document.createElement('div');
                    div.setAttribute('class', 'each_places_from_list');
                    div.classList.add('places__list')
                    div.setAttribute('onclick', "selectplace(this)");
                    div.setAttribute('data-value', element.code)
                    div.innerText = `${element.city} (${element.country})`;
                    list.append(div);
                })
            })
    }
}

/**
 * The function `flight_to` is used to handle user input for selecting a flight destination and
 * fetching relevant places based on the input.
 * @param event - The `event` parameter in the `flight_to` function is an event object that represents
 * an event being handled, such as a keypress or input event. It is typically passed to the function
 * when it is called in response to an event listener being triggered.
 * @param [focus=false] - The `focus` parameter in the `flight_to` function is a boolean parameter that
 * determines whether the input field should retain its value or be cleared when the function is
 * called. If `focus` is `true`, the input field will retain its value. If `focus` is `false`, the
 */
function flight_to(event, focus = false) {
    let input = event.target;
    let list = document.querySelectorAll('#places_to');
    showplaces(input);

    if (!focus) {
        input.dataset.value = "";
    }

    if (input.value.length > 0) {
        fetch('query/places/' + input.value)
            .then(response => response.json())
            .then(places => {
                list.innerHTML = '';
                places.forEach(place => {
                    let div = document.createElement('div');
                    div.setAttribute('class', 'each_places_from_list');
                    div.classList.add('places__list')
                    div.setAttribute('onclick', "selectplace(this)");
                    div.setAttribute('data-value', element.code)
                    div.innerText = `${element.city} (${element.country})`;
                    list.append(div);
                })
            })
    }
}

function hideplaces(input) {
    let box = input.parentElement.querySelector(".places_box");
    setTimeout(() => {
        box.style.display = 'none';
    }, 300);
}

function showplaces(input) {
    let box = input.parentElement.querySelector('.places_box');
    if (box) {
        box.style.display = 'block';
        console.log('sahi hai')
    } else {
        console.log("box is null");
    }
}

/**
 * The function `select_place` sets the value of an input field to the uppercase value of a selected
 * option and stores the original value in a dataset attribute.
 * @param option - The `option` parameter in the `select_place` function is typically a reference to
 * the HTML element that triggered the function. It is usually an option element within a select
 * dropdown that the user has selected.
 */

function selectplace(option) {
    let input = option.closest('.input-row').querySelector('input[type="text"]');
    console.log("Hellooooo");
    if (input) {
        input.value = option.dataset.value.toUpperCase();
        input.dataset.value = option.dataset.value;
        console.log(input.value);
    } else {
        console.error('Input element not found.');
    }
}



function trip_type() {
    document.querySelectorAll('.trip-type').forEach(type => {
        if (type.checked) {
            if (type.value === "1") {
                document.querySelector('#return_date').value = '';
                document.querySelector('#return_date').disabled = true;
            }
            else if (type.value === "2") {
                document.querySelector('#return_date').disabled = false;
            }
        }
    })
}

/**
 * The function `flight_search` validates user input for a flight search form, ensuring required fields
 * are filled before proceeding.
 * @returns The `flight_search()` function is returning `false` in case any of the validation checks
 * fail, indicating that the flight search cannot proceed due to missing information or incorrect
 * selections.
 */
function flight_search() {
    if (!document.querySelector("#flight-from").dataset.value) {
        alert("Please select flight origin.");
        return false;
    }
    if (!document.querySelector("#flight-to").dataset.value) {
        alert("Please select flight destination.");
        return false;
    }
    if (document.querySelector("#one-way").checked) {
        if (!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
    }
    if (document.querySelector("#round-trip").checked) {
        if (!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
        if (!document.querySelector("#return_date").value) {
            alert("Please select return date.");
            return false;
        }
    }
}