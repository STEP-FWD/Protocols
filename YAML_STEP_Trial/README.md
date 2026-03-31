## Working with YAML Protocol writing 
The guide is first made to see whether the YAML structure has potential or it is too complicated for our purpose. 
For this, we will first start by showing how to use the structure locally, to beta test it. 
### Installation of packages. 
First you need to have in your computer python and MkDocs (https://www.mkdocs.org/)

### Organizing the structure 
Now in the folder where you store your python files make the structure as it is in this folder (You could just copy this folder directly)::

- docs 
    - Protocol_X.yaml
    - protocol_Y.yaml
    - index.md
- YAML_comvert.py
- mkdocs.yaml
- README.md

#### What does each file do? 
- mkdocs: is the leading file. This will create the "website" of the project.
- YAML_convert: this is the parser from the protocol YAML to the protocol md, which is what mkdocs understands. What this will do when runnning it is create mew files in the docs folder, for example, from protocol_X.yaml it will create protocol_x.md.
- index.md is the homepage of the mkdocs created "web". This

### How to fill the yaml protocol? 
As we are using a parser to translate from YAML to MD, the protocol needs to be written in a very specific way. If this is not done, some information will be missing. 
- First of all the folder structure right now has to be what is mentioned above. Importantly the begining of the parser has a folder variable, in which you should write the path to your "docs" folder, created above. Otherwise it will not see the files. 
- Secondly the steps of the protocol have to be written as in the protocol template. For example for writing the materials and methods you have to write "materials: Write your materials", you cannot write something different like "m&m", "mat", etc. It has to be "materials: whatever".
The same applies to all the other variables. Following the template is essential to make the parser work.
- Thirdly for the inheriting the same applies. I will put a template for inheriting. The cool thing here is you can write
    - inherits_from: template_1
    - modifications:
      - step_id:2.2 ### Then you just modify the steps you want and it keeps the rest of the protocol.


### Tricks with YAML
Help for writing YAML: [https://learntheweb.courses/topics/markdown-yaml-cheat-sheet/](https://learntheweb.courses/topics/yaml/)
