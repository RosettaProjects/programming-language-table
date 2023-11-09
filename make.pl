#!/usr/bin/perl -I ./modules

use strict; 
use warnings; 
use sync;
use table;
use html;
  
print("\nGenerating site HTML\n"); 

sync::FeatView2LangView();
sync::LangView2FeatView();

table::BuildTable();

output = html::InterpolateHTML();
html::WriteHTML();

print("\nSaved generated HTML doc to ./docs/_build/index.html\n\n");
