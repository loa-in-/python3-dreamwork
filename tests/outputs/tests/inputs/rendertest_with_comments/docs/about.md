>    # Weave and Tangle

>   ## Introduction

>   Welcome to the example code of a fictitious project called |Whitespace
Handling Test|.

>   ### Definitions

>   Short phrases, like the name of the project:

          ************************************************************          
       Definition of name of the project
          ------------------------------------------------------------          
Whitespace Handling Test
          ************************************************************          

>   Whole definitions with arbitrary whitespace:

          ************************************************************          
       Definition of mkdocs nav section entries
          ------------------------------------------------------------          
- About: about.md
- Generating Python: python.md
- Improving JavaScript: javascript.md

          ************************************************************          

          ************************************************************          
       Definition of mkdocs nav section
          ------------------------------------------------------------          
nav:
    - Configuring Apache and MySQL: webconfig.md
    - Configuring Apache and MySQL: webconfig.md
    

          ************************************************************          

>   #### Extending definitions both ways

          ************************************************************          
       Definition of mkdocs nav section entries
          ------------------------------------------------------------          
- Configuring Apache and MySQL: webconfig.md

          ************************************************************          

>   ### References

>   The file this chapter will be written to is `|docs/webconfig.md|`.

>   ### Files

          ************************************************************          
       Definition of file:mkdocs.yml
          ------------------------------------------------------------          
site_name: Whitespace Handling Test
nav:
    nav:
        - Configuring Apache and MySQL: webconfig.md
            - Configuring Apache and MySQL: webconfig.md
            
    


          ************************************************************          

>   ## Pieceing it together

>   How to configure mkdocs to use another theme? We won't use it but here, look
for yourself:

          ************************************************************          
       Definition of possible extension of actual file
          ------------------------------------------------------------          
site_name: Whitespace Handling Test
nav:
    nav:
        - Configuring Apache and MySQL: webconfig.md
            - Configuring Apache and MySQL: webconfig.md
            
    


theme: readthedocs

          ************************************************************          

>   ### Weaving

>   Something about weaving

>   ### Tangling

>   Something about tangling

