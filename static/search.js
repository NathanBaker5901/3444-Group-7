//Making the search functionality in the search bar

// array for the search bar go into the array
let users = []

// Makes the search bar working
const searchInput = document.querySelector("[data-search]")
searchInput.addEventListener("input", e => {
    const value = e.target.value
    console.log(value)
})