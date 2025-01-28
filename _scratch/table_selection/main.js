/* Desired behavior: 
- default languages shown at start
- category selected: all included languages selected (OR logic)
- category unselected: all included languages selected if not still covered by other selected categories
- language/row selected: no side effect; categories unchanged (i.e. language/row un-/selection overrides category selections)
- language/row selected: unselected, unless implied by a selected category
*/

const table = document.getElementById("categoryTable");
const rowNames = Object.freeze(Array.from(document.querySelectorAll('.row_menu input[type="checkbox"]')).map(input => input.value));
const colNames = Object.freeze(Array.from(document.querySelectorAll('.col_menu input[type="checkbox"]')).map(input => input.value));
// console.log("rowNames", rowNames);
// console.log("colNames", colNames);

const langClasses = {
    compiled: ['rust', 'haskell'],
    interpreted: ['python', 'haskell'],
};
const subsections = {
    '0': ['0.0'],
    '0.1': ['0.1.0', '0.1.1']
};

const categoryHierarchy = {
    prim_types: ['integer', 'boolean'],
};

// FUNCTIONS ==========================================================================================================

function getCheckboxValues(className) {
    return Array.from(document.querySelectorAll(`.${className} input[type="checkbox"]`))
        .filter(input => input.checked)
        .map(input => input.value);
}

function computeLanguages() {
    const selectedLanguages = getCheckboxValues('col_menu')
    console.log('selectedLanguages', selectedLanguages)

    return [...new Set(selectedLanguages.flatMap(item => langClasses[item] || item))];
}

function computeRows() {
    const selectedRows = getCheckboxValues('row_menu')
    console.log('selectedRows', selectedRows)

    return [...new Set(selectedRows.flatMap(item => [item].concat(subsections[item] || [item])))];
}

function toggleOutput() {
    document.querySelectorAll('.output').forEach(el => {
        if (el.textContent === '') {
            text = el.getAttribute('data-original');
            el.innerHTML = `<br><span class="output_prefix">❯&nbsp;</span><span class="output_substance">${text}</span>`;
        } else {
            el.setAttribute('data-original', el.innerHTML
                .replace(/^<br><span class="output_prefix">❯&nbsp;<\/span><span class="output_substance">/g, '')
                .replace(/^<\/span>/g, '')
            );
            el.textContent = '';
        }
    });
}

function toggleBoilerplate() {
    document.querySelectorAll('.boilerplate').forEach(el => {
        if (el.textContent === '') {
            text = el.getAttribute('data-original');
            el.innerHTML = `${text}<br>`;
        } else {
            el.setAttribute('data-original', el.textContent);
            el.textContent = '';
        }
    });

    document.querySelectorAll('.indent_if_bp').forEach(el => {
        if (el.innerHTML.startsWith('&nbsp;&nbsp;&nbsp;&nbsp;')) {
            el.innerHTML = el.innerHTML.replace(/^&nbsp;&nbsp;&nbsp;&nbsp;/g, '');
        }
        else {
            el.innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;' + el.innerHTML;
        }
    });
}

function updateChildLanguages(selectedLangs) {
    document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
        if (selectedLangs.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });
}

function updateChildRows(selectedRows) {
    document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
        if (selectedRows.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });
}

function deselectChildRows(rowID) {
    if (rowID in subsections) {
        const toDeselect = subsections[rowID];
        document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
            if (toDeselect.includes(checkbox.value)) {
                checkbox.checked = false;
            }
        });
    }
}

function deselectChildLanguages(colID) {
    if (colID in langClasses) {
        const toDeselect = langClasses[colID];
        document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
            if (toDeselect.includes(checkbox.value)) {
                checkbox.checked = false;
            }
        });
    }
}

function filterTableRows() {
    const selectedRows = computeRows();
    console.log('selectedRows', selectedRows);
    updateChildRows(selectedRows);

    table.querySelectorAll("tbody tr").forEach(row => {
        const rowCategories = row.dataset.category.split(" ");
        const hasMatch = rowCategories.some(category => selectedRows.includes(category));
        row.classList.toggle("hidden", !hasMatch);
    });
}


function filterLanguages() {
    selectedLanguages = computeLanguages();
    console.log(selectedLanguages);
    updateChildLanguages(selectedLanguages);
    const columnIndexesToHide = [];

    table.querySelectorAll("thead th").forEach((th, colIndex) => {
        if (colIndex > 0) {
            const colCategory = th.dataset.category;
            const shouldHide = !selectedLanguages.includes(colCategory);
            if (shouldHide) {
                columnIndexesToHide.push(colIndex);
            }
            th.classList.toggle("hidden", shouldHide);
        }
    });

    table.querySelectorAll("tbody tr").forEach(row => {
        row.querySelectorAll("td").forEach((td, colIndex) => {
            if (colIndex > 0) {
                const shouldHide = columnIndexesToHide.includes(colIndex);
                td.classList.toggle("hidden", shouldHide);
            }
        });
    });
}

// EVENT LISTENERS ====================================================================================================

document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener("change", (event) => {
        if (event.target.checked) {
            filterTableRows();
        } else {
            deselectChildRows(event.target.value);
            filterTableRows();
        }
    })
});

document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener("change", (event) => {
        if (event.target.checked) {
            filterLanguages();
        } else {
            deselectChildLanguages(event.target.value);
            filterLanguages();
        }
    })
});

document.getElementById('boilerplateToggle').addEventListener('change', toggleBoilerplate);

document.getElementById('outputToggle').addEventListener('change', toggleOutput);

document.querySelectorAll('.dropdown button').forEach(button => {
    button.addEventListener('click', () => {
        const dropdown = button.parentElement;
        dropdown.classList.toggle('open');
    });
});

document.addEventListener('click', (e) => {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });
});

// INITIALIZATION =====================================================================================================