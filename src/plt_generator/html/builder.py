from ..highlighting import SyntaxHighlighter
from ..data.master_table import MasterTable

header = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProgLang Table</title>
    <link rel="stylesheet" href="style.css" type="text/css">
</head>

<body>


    <div class="buttons">
        <div class="dropdown">
            <button id="helpButton" class="foldout">Help / Information</button>
            <div class="dropdown-menu selection text_field">
                <b>Keyboard shortcuts</b>:<br><br>
                &nbsp;&nbsp;<span class="keyName"><b>b&nbsp;</b></span> toggle boilerplate<br>
                &nbsp;&nbsp;<span class="keyName"><b>i&nbsp;</b></span> show help (information/instructions)<br>
                &nbsp;&nbsp;<span class="keyName"><b>o&nbsp;</b></span> toggle output<br>
                &nbsp;&nbsp;<span class="keyName"><b>p&nbsp;</b></span> toggle output prefix<br>
                &nbsp;&nbsp;<span class="keyName"><b>t&nbsp;</b></span> toggle title<br>

                &nbsp;&nbsp;<span class="keyName"><b>r&nbsp;</b></span> open row selection menu<br>
                &nbsp;&nbsp;<span class="keyName"><b>c&nbsp;</b></span> open language (column) selection menu<br>
                <!-- &nbsp;&nbsp;<span class="keyName"><b>h&nbsp;</b></span> move left<br> -->
                &nbsp;&nbsp;<span class="keyName"><b>j&nbsp;</b></span> move down<br>
                &nbsp;&nbsp;<span class="keyName"><b>k&nbsp;</b></span> move up<br>
                <!-- &nbsp;&nbsp;<span class="keyName"><b>l&nbsp;</b></span> move right<br> -->
                &nbsp;&nbsp;<span class="keyName"><b>&lt;space&gt;&nbsp;</b></span> toggle currently selected item<br>

                <br><br><b>Note</b>: For the menus, either use the mouse, or use the keyboard navigation, but not both.
                It doesn't work well to mix them, and I don't see a compelling reason to prioritize fixing this.


            </div>
        </div>

        <div id="rowFilter" class="dropdown">
            <button id="rowsButton" class="foldout">Features (Rows)</button>
            <div class="dropdown-menu selection row_menu">
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0">
                    <span class="checkbox_text"><b>Basic</b></span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0.0">
                    <span class="checkbox_text"><b>&nbsp;&nbsp;Console Output</b></span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0.0.0">
                    <span class="checkbox_text">&nbsp;&nbsp;&nbsp;&nbsp;Hello, world!</span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0.1">
                    <span class="checkbox_text"><b>&nbsp;&nbsp;Primitive Types</b></span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0.1.0">
                    <span class="checkbox_text">&nbsp;&nbsp;&nbsp;&nbsp;Boolean</span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="0.1.1">
                    <span class="checkbox_text">&nbsp;&nbsp;&nbsp;&nbsp;Integer</span>
                </label>
            </div>
        </div>

        <div id="columnFilter" class="dropdown">
            <button id="columnsButton" class="foldout">Languages (Columns)</button>
            <div class="dropdown-menu selection col_menu">
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="interpreted">
                    <span class="checkbox_text"><b>Interpreted</b></span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="compiled">
                    <span class="checkbox_text"><b>Compiled</b></span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="python">
                    <span class="checkbox_text">Python</span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="rust">
                    <span class="checkbox_text">Rust</span>
                </label>
                <label class="checkbox_label">
                    <input type="checkbox" checked="true" value="haskell">
                    <span class="checkbox_text">Haskell</span>
                </label>
            </div>
        </div>

        <div id="displayOptions" class="dropdown">
            <button id="displayButton">Display Options</button>
            <div class="dropdown-menu display_menu">
                <label class="checkbox_label">
                    <input id="boilerplateToggle" type="checkbox" value="showBoilerplate">
                    <span class="checkbox_text">Show boilerplate</span>
                </label>
                <label class="checkbox_label">
                    <input id="outputToggle" type="checkbox" value="showOutput">
                    <span class="checkbox_text">Show output</span>
                </label>
                <label class="checkbox_label">
                    <input id="outputPrefixToggle" type="checkbox" value="showOutputPrefix">
                    <span class="checkbox_text">Show output</span>
                    prefix</label>
                <label class="checkbox_label">
                    <input id="titleToggle" type="checkbox" value="hideTitle">
                    <span class="checkbox_text">Hide title</span>
                </label>
            </div>
        </div>
    </div>

    <div id="title">
        <h1>Programming Language Table</h1>
    </div>

'''

footer = '''

    <script src="main.js">


    </script>


</body>

</html>
'''

class HTMLBuilder:
    def __init__(self, highlighter: SyntaxHighlighter) -> None:
        self.highlighter: SyntaxHighlighter = highlighter

    def __call__(self, master_table: MasterTable) -> str:
        languages = master_table.languages
        rows = master_table.rows
        table = ""
        return f"{header}{table}{footer}"
