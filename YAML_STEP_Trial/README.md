## Working with YAML Protocol writing 
- The guide is first made to see whether the YAML structure has potential or it is too complicated for our purpose. 
- For this, the first step is to show how to use the structure **locally**, to beta test it.
### Protocol to make the structure run in your computer 
- Step 1. Cloning this folder in your personal PC and make it work there.
- Step 2. Running the codes. To make the mkdocs website you have to do the following:
      - Open your terminal. I use Anaconda so I generally use Anaconda_prompt, so I ensure my pythonpath works
      - Change directory to the directory of this folder (the code has to see the mkdocs.yaml file). In my case this is: "C:\Users\jdiez\Documents\GitHub\Protocols\YAML_STEP_Trial", so I run cd C:\Users\jdiez\Documents\GitHub\Protocols\YAML_STEP_Trial
      - Once in the directory run: mkdocs serve. This will now run the server of the website. You can acces it by copying: http://127.0.0.1:8000/ in your preferred browser.
- Step 3. Now you are seeing the database. In case you want to change some protocol you would have to write a new YAML protocol (copy and modify the template_protocol.yaml), for easeness.
- Step 4. Everytime you write a new protocol you have to:
    - Run the YAML converter (YAML_convert.py). You can run this directly in your preferred python interpreter (Spyder, Visual Studio Code) or in the terminal
    - Now this will create a protocol.md from your new protocol.
    - In order for the database to see this new file, you have to modify the mkdocs.yml, to add the new protocol (*I will update this so that some point is automatic*)
    - If you want to modify the home page to show these new protocol, you can modify index.md. (*Again at some point this can be made to be automatic when parsing the new yaml file*)
    - 
### Installation of packages. 
You need to have in your computer python and MkDocs (https://www.mkdocs.org/)

### Organizing the structure 
The folder to run this should be in "pythonpath". For ease of use I put this folder inside my general python folder, so I make sure that it runs. The structure that you have should be exactly as as it is in this folder (that's why directly cloning this would be the best approach). Just to clarify the structure has to be as follows: 
- folder where python works: 
    |- docs 
        |- Protocol_X.yaml
        |- protocol_Y.yaml
        |- index.md
    |- YAML_comvert.py
    |- mkdocs.yaml
    |- README.md

#### Explanation of the files 
- mkdocs: is the leading file. This will create the "website" of the project. It includes the basic architecture of the website. 
- YAML_convert: this is the parser from the protocol YAML to the protocol md, which is what mkdocs understands. What this will do when runnning is create mew files in the docs folder, for example, from protocol_X.yaml it will create protocol_x.md. The parser has to be made very robust to have a reliable structure. *I am still working on it*
- index.md is the markdown which creates the homepage of the mkdocs created "web". This has for example the navigation of the database. 

### Filling the yaml protocol 
As we are using a parser to translate from YAML to MD, the protocol needs to be written in a very specific way. If this is not done properly, some information will be missing. 
- First of all the folder structure right now has to be what is mentioned above. Importantly the begining of the parser has a folder variable, in which you should write the path to your "docs" folder, created above. Otherwise it will not see the files. *I am going to try to make it general so it works directly on whatever folder it is placed* 
- The steps of the protocol have to be written as in the protocol template. For example for writing the materials and methods you have to write "materials: Write your materials", you cannot write something different like "m&m", "mat", etc. It has to be "materials: whatever". The same applies to all the other variables. Following the template is essential to make the parser work.
- The same goes for the for the inheriting. The cool thing here is you can write
    - inherits_from: template_1
    - modifications:
      - step_id:2.2 ### Then you just modify the steps you want and it keeps the rest of the protocol.


### Tricks with YAML
Help for writing YAML: [https://learntheweb.courses/topics/markdown-yaml-cheat-sheet/](https://learntheweb.courses/topics/yaml/)
