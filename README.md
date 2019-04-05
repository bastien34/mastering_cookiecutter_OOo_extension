Configurator Tool Extension
===========================

# Features
Allow to easily configure a new extension project. Creates Addons like menubar,
toolbar and options dialog as well.

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter).

# Usage
First, get Cookiecutter. Great people says it's awesome!

    $ pip3 install --user "cookiecutter>=1.4.0"

Clone this repo (don't try to just download extension_generator.odt, it won't work!). 
If you don't see `extension_generator.odt`, create it with the command:

    $ ./odt_gen.py
    
Then copy the `extension_generator.odt` in your working directory. Your extension
will be created next to it, in the same folder.

Open it and activate the macro. Fulfill the tables describing your extension. See
below for details.

Click the button "GENERATE EXTENSION". That's it!

# What's you gonna have?

The macro run a script against [cookiecutter_ooo_extension](https://github.com/bastien34/cookiecutter_ooo_extension).
It will generate for you all the boilerplate of the extension you want to work on. Here
is the layout of the project:

```
├── my_extension
│   ├── extension
│   ├── src
│   └── README.md
```

You can test the created extension generated in `extension/`. It contains options 
dialog for options you defined in `extension_generator.odt`, menubar and toolbar.

Start coding in the `src/` directory. Your python code should be located at 
 `src/python/` in the module `your_extension.py`.
 
# How to compile my extension?

TODO: Once you're code is ready, you'll find a tool in the src to compile your code. 
Dont' use the `extension_generator`, it would erase your previous work !

# TODO:

- Documentation for WINDOWS OS.

- Handle images (toolbar and extension). Means passing to cookiecutter your working
directory to find statics and integrate them into your project.

- Yep, it's a shame! For now supports only **string** and **boolean** types ! No
more time to develop further !

- Handle LICENSE, README, EXTENSION DESCRIPTION... 

- Document how to translate !!!

# It doesn't work? 

Are you using Windowns operating system? We need you to document the installation 
(as well of IOs). It works out of the box on Ubuntu OS with LibreOffice.

To debug or understand what's going on, it's important you run LibreOffice from the
command line. You'll see error logs. It might help since we created some exceptions (see below).

You advocate to activate (at least) the INFO level logger to see what's going on.

We handle some exception:

**ImageNotFoundError**

    Not implemented yet as said.

**FunctionTypeNotSupportedError**

    For now, we support only `string` and `boolean`. If you misspell it, it will
    raise **FunctionTypeNotSupportedError**.


# Technical details

### General Vars
|Keys               | Default values                      | Note         |
| ---               | ---                                 |---              |
|extension_name     | my_extension                        |No blank space
|extension_label    | My extension                        |Displayed in menu
|extension_version  | 0.0.1                               |
|package_name       | com.mycompany.my_extension          |Identifier, see below the schema to assure uniqueness
|company_name       | Your Company                        |
|author_name        | Your Name                           |
|author_email       | your_mail@provider.com              |
|update_url         | pointing to your update.xml file    |URL
|release_note_url   | pointing to your release note       |URL
|publisher_url      | https://yourwebsite.com             |URL
|image_name         | logo.png                            |PNG or JPG, 42x42 pixels


### Full detail of the project source
As said, 2 dirs (`src/` and `extension`) are created in the output directory. 

#### Treeview of the `src/` content

```
├── AddonUI.xcu
├── config
│   ├── {{cookiecutter.extension_name}}_config.xcs
│   ├── {{cookiecutter.extension_name}}_dialog.xcu
│   └── {{cookiecutter.extension_name}}_options.components
├── Descriptions
│   ├── descr-en.txt
│   ├── descr-fr-FR.txt
│   └── descr-fr.txt
├── description.xml
├── dialogs
│   └── {{cookiecutter.extension_name}}_dialog.xdl
├── icons
│   ├── bal_16.png
│   └── excel_16.png
├── images
│   └── logo.png
├── META-INF
│   └── manifest.xml
├── oxt_gen.py
├── python
│   ├── {{cookiecutter.extension_name}}_dialog_handler.py
│   ├── {{cookiecutter.extension_name}}.py
│   └── pythonpath
│       ├── {{cookiecutter.extension_name}}
│       │   ├── options_dialog.py
│       │   └── __pycache__
│       ├── {{cookiecutter.extension_name}}_utils.py
│       └── locales
│           └── fr_FR
│               └── LC_MESSAGES
│                   ├── messages.mo
│                   └── messages.po
└── WindowState
    └── tbWriter.xcu
```

### Filenames coding
You'll find a file description here: 
https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/File_Format

We use `{{cookiecutter.extension_name}}` in filename to keep things distinct and 
well organized. If you have many extensions, each one with a config.xcu, it 
might be difficult to find straight away which project it belongs to.


|File     | Note                      | Location         |
| ---       | ---                                 |---              |
|dialog.xdl     | Content of graphic Windows, build using the LibO dialog editor. (290x215 max)|dialogs/{{cookiecutter.extension_name}}_dialog.xdl
|manifest.xml    | Contains appropriate entry for modules, configuration data.      |META-INF/manifest.xml
|config.xcs    | Configuration schema of your vars.      |config/{{cookiecutter.extension_name}}_config.xcs
|dialog.xcu   | Configuration data file gives location for executables and dialog box.      |config/{{cookiecutter.extension_name}}_dialog.xcu
|options.component| Dialog handler location and implementation name | config/{{cookiecutter.extension_name}}_options.component
|dialog_handler.py| Dialog handler file | python/{{cookiecutter.extension_name}}_dialog_handler.py
|module.py| File where you'll start working on your code. Contains a simple launcher. | python/{{cookiecutter.extension_name}}.py
|description.xml| Description of your extension. See below. |  description.xml
|AddonUI.xcu| Toolbars and Menubar. |  AddonUI.xcu


#### Options Dialog Window
This `.xdl` file contains the description of the graphic Windows. We build it 
using the LibO dialog editor.

The size of the windows should be something like width: 290, height: 215.

It may not have the “OK”, “CANCEL”, “HELP” or “Back” buttons. These buttons are 
already part of OOo's options dialog and the options dialog created by the 
Extension Manager.


#### manifest.xml
An extension needs to provide configuration data (xcu files) in order to define 
modules, nodes and leaves. These files can be anywhere in the extension, except 
in META-INF, and there must be an appropriate entry in the manifest-xml.

#### Config file: `{{cookiecutter.extension_name}}_config.xcs`
The configuration Schema file gives important information on your vars. For this
first version, I let personal stuff. It's up to you to adapt it manually to
your needs.

Important var here is `oor:package="{{cookiecutter.package_name}}`

#### Config file: `{{cookiecutter.extension_name}}_dialog.xcu`
The configuration data file gives location for executables, for the dialog box. 

Contains:

- Nodes name: defined as: {{cookiecutter.package_name}}.Node1. 
(e.g.: `com.mycompany.myextension.node1`)

- Nodes label: defined as: {{cookiecutter.extension_label}} (e.g.: `My Extension`)

- Leaves name: {{cookiecutter.package_name}} After multiple experiment, it seems 
that it is here the unique identifier as said above: "Every leaf has exactly one 
Options page and is assigned to exactly one Node and one Dialog".

- Leaves id: {{cookiecutter.package_name}} (See Identifier section before)

- EventHandler Service: `{{cookiecutter.package_name}}.service`


#### Config file: `{{cookiecutter.extension_name}}_options.component`
This file gives the dialog handler location (seen before) and the implementation 
name.

- Implementation name: `{{cookiecutter.package_name}}.IM` 

- Event handler Service name: see `.xcu` config file

#### Dialog handler File: launcher of the options feature
This file uses the already configured implementation name and event handler
service name as defined above.

#### {{cookiecutter.extension_name}}.py
The file where you'll create your fantastic code. For now, we let here a
Environ class that handle all var.

#### Description: description.xml
- Company name: Your company name `{{cookiecutter.company_name}}`

- Author name: your name `{{cookiecutter.author_name}}`

- Author email: your email `{{cookiecutter.author_email}}`

- Package name: `{{cookiecutter.package_name}}` as said, **reversed_domainname
.company.product.nodename.leafname.**
which can be `com.mycompany.myextension`

- Project version: `{{cookiecutter.extension_version}}` e.g.: "0.0.1"

- Image name: `{{cookiecutter.image_name}}` Images are in `images/` folder. 
42x42. eg: `my_image.jpg` JPG or PNG can be used.

- Update URL: `{{cookiecutter.update_url}}` 

- Publisher URL: your website

- Release note url. 


#### AddonUI.xcu
File that contains everything to create toolbars and Menubar. 


## Localization

Localization (`messages.po`) are located in `python/pythonpath/locales`.
 
We used 'xgettext' to generate our template as following:

`find . -name "*.py" > potfiles`

`xgettext -n --files-from potfiles -d python/pythonpath/locales/messages `

Then you can delete the 'potfiles'.

### .po file from .xml files

Create a file `rule.its` with this content. See [this](https://stackoverflow.com/questions/55270068/its-rule-to-translate-a-xml-attribute-using-namespace/55275811#55275811)
to understand why you need to declare the namespace in it.

    <?xml version="1.0"?>
    <its:rules xmlns:its="http://www.w3.org/2005/11/its" version="1.0" 
               xmlns:dlg="http://openoffice.org/2000/dialog">
      <its:translateRule selector="//dlg:text/@dlg:value" translate="yes"/>
    </its:rules>

Then generate the `.po` file using `itstool`.

    $  itstool -o message_from_dialog.po -i rule.its dialogs/dialog.xdl
    
You'll have to merge them to existent message.po.
