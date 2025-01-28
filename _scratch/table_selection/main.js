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

function toggleOutput(isSelected) {
    if (isSelected) {
        document.querySelectorAll('.output_cell').forEach(cell => {
            cell.classList.remove("hidden");
        });
    }
    else {
        document.querySelectorAll('.output_cell').forEach(cell => {
            cell.classList.add("hidden");
        });
    }
}

function toggleOutputPrefix(isSelected) {
    if (isSelected) {
        document.querySelectorAll('.output_prefix').forEach(cell => {
            cell.classList.remove("hidden");
        });
    }
    else {
        document.querySelectorAll('.output_prefix').forEach(cell => {
            cell.classList.add("hidden");
        });
    }
}

function toggleTitle(isSelected) {
    const titleBlock = document.getElementById('title');
    const tableBlock = document.getElementById('table-container');
    if (isSelected) {
        titleBlock.classList.add("hidden");
        tableBlock.style.top = '4rem';
    }
    else {
        titleBlock.classList.remove("hidden");
        tableBlock.style.top = '8rem';
    }
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

    table.querySelectorAll("thead th").forEach(th => {
        if (!th.classList.contains('row_name')) {
            if (selectedLanguages.includes(th.dataset.category)) {
                th.classList.remove("hidden");
            }
            else {
                th.classList.add("hidden");
            }
        }
    });

    table.querySelectorAll("tbody tr").forEach(row => {
        row.querySelectorAll("td").forEach(td => {
            console.log(td)
            if (!td.classList.contains('row_name')) {
                if (selectedLanguages.includes(td.dataset.category)) {
                    td.classList.remove("hidden");
                }
                else {
                    td.classList.add("hidden");
                }
            }
            else { console.log("nothing");}
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

document.getElementById('outputToggle').addEventListener('change', (event) => {
    toggleOutput(event.target.checked);
});

document.getElementById('outputPrefixToggle').addEventListener('change', (event) => {
    toggleOutputPrefix(event.target.checked);
});

document.getElementById('titleToggle').addEventListener('change', (event) => {
    toggleTitle(event.target.checked);
});

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

toggleOutput(false);
toggleOutputPrefix(false);
