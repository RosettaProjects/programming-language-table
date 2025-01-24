Yes, you can use JavaScript to dynamically change CSS variables. CSS variables (also known as custom properties) are defined in stylesheets or inline styles using the -- prefix and can be accessed and modified with JavaScript through the style property or the setProperty method of the style object.

Example of Changing CSS Variables with JavaScript
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Change CSS Variables</title>
    <style>
        :root {
            --primary-color: blue;
            --secondary-color: orange;
        }

        body {
            background-color: var(--primary-color);
            color: var(--secondary-color);
            transition: background-color 0.3s, color 0.3s;
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <button id="change-theme">Change Theme</button>

    <script>
        // JavaScript to dynamically change CSS variables
        const button = document.getElementById("change-theme");

        button.addEventListener("click", () => {
            // Access the root element (the :root pseudo-class)
            const root = document.documentElement;

            // Change CSS variables
            root.style.setProperty("--primary-color", "black");
            root.style.setProperty("--secondary-color", "white");
        });
    </script>
</body>
</html>
```

How It Works:
Define CSS Variables:

CSS variables are defined inside the :root pseudo-class or any selector.
Example: --primary-color and --secondary-color.
Modify CSS Variables with JS:

Use document.documentElement.style.setProperty() to modify variables globally.
Syntax: element.style.setProperty('--variable-name', 'value').
Dynamic Styling:

When you update the CSS variable, all elements using that variable automatically update.
Accessing CSS Variables in JavaScript
You can also retrieve the current value of a CSS variable using getComputedStyle:

javascript
Copy
Edit
const root = document.documentElement;
const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();
console.log(primaryColor); // Logs the current value of --primary-color
Use Cases:
Theming: Easily switch between light/dark mode.
Dynamic Layouts: Adjust spacings, sizes, or colors based on user interaction.
Animations: Update variables during animations for smooth transitions.
Let me know if you'd like an example for a specific use case!

----

Here's a solution using JavaScript to filter an HTML table so only certain rows and columns are displayed, based on categories selected via a dropdown menu.

Steps:
Create an HTML table with data-* attributes for rows and columns.
Add two multi-select dropdown menus: one for rows and one for columns.
Use JavaScript to update the table's visibility based on the selected categories.
Example Code:
HTML:
html
Copy
Edit
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Table Filter</title>
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 8px;
      text-align: center;
    }
    .hidden {
      display: none;
    }
  </style>
</head>
<body>
  <h1>Filter Table by Categories</h1>

  <label for="rowFilter">Select Row Categories:</label>
  <select id="rowFilter" multiple>
    <option value="A">A</option>
    <option value="B">B</option>
    <option value="C">C</option>
  </select>

  <label for="columnFilter">Select Column Categories:</label>
  <select id="columnFilter" multiple>
    <option value="D">D</option>
    <option value="E">E</option>
    <option value="F">F</option>
  </select>

  <table id="categoryTable">
    <thead>
      <tr>
        <th>Row/Col</th>
        <th data-category="D">D</th>
        <th data-category="E">E</th>
        <th data-category="F">F</th>
      </tr>
    </thead>
    <tbody>
      <tr data-category="A">
        <td>A</td>
        <td>1</td>
        <td>2</td>
        <td>3</td>
      </tr>
      <tr data-category="B">
        <td>B</td>
        <td>4</td>
        <td>5</td>
        <td>6</td>
      </tr>
      <tr data-category="C">
        <td>C</td>
        <td>7</td>
        <td>8</td>
        <td>9</td>
      </tr>
    </tbody>
  </table>

  <script>
    const rowFilter = document.getElementById("rowFilter");
    const columnFilter = document.getElementById("columnFilter");
    const table = document.getElementById("categoryTable");

    function filterTable() {
      const selectedRows = Array.from(rowFilter.selectedOptions).map(option => option.value);
      const selectedColumns = Array.from(columnFilter.selectedOptions).map(option => option.value);

      // Filter rows
      table.querySelectorAll("tbody tr").forEach(row => {
        const rowCategory = row.dataset.category;
        row.classList.toggle("hidden", !selectedRows.includes(rowCategory));
      });

      // Filter columns
      const columnIndexesToHide = [];
      table.querySelectorAll("thead th").forEach((th, colIndex) => {
        if (colIndex > 0) { // Skip first column header (Row/Col)
          const colCategory = th.dataset.category;
          const shouldHide = !selectedColumns.includes(colCategory);
          columnIndexesToHide.push(shouldHide ? colIndex : null);
          th.classList.toggle("hidden", shouldHide);
        }
      });

      table.querySelectorAll("tbody tr").forEach(row => {
        row.querySelectorAll("td").forEach((td, colIndex) => {
          td.classList.toggle("hidden", columnIndexesToHide.includes(colIndex));
        });
      });
    }

    // Attach event listeners
    rowFilter.addEventListener("change", filterTable);
    columnFilter.addEventListener("change", filterTable);

    // Initialize filter
    filterTable();
  </script>
</body>
</html>
Explanation:
Dropdown Menus:

rowFilter selects which rows to show, based on their data-category attributes.
columnFilter selects which columns to show, based on data-category attributes in the <th> elements.
JavaScript Filtering:

Rows: Use the hidden class to hide rows whose category is not selected.
Columns: Hide columns by looping through <th> and corresponding <td> elements.
Dynamic Updates:

When dropdown values change, filterTable() updates the visibility of rows and columns.
You can now select multiple categories from the dropdown menus, and the table will dynamically update to show only the selected rows and columns.