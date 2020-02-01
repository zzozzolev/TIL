## Redirections
- https://catonmat.net/bash-one-liners-explained-part-three

## What does &> do in bash?
- https://stackoverflow.com/questions/24793069/what-does-do-in-bash

## about #!/bin/bash
- http://forum.falinux.com/zbxe/index.php?document_srl=541629&mid=lecture_tip

## shell style guide
- https://google.github.io/styleguide/shell.xml

## functions
- https://ryanstutorials.net/bash-scripting-tutorial/bash-functions.php

## Exit Codes
- https://bencane.com/2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts/

## Meaning of $? in shell scripts
- https://stackoverflow.com/questions/7248031/meaning-of-dollar-question-mark-in-shell-scripts

## echo
```
#You can also use echo to remove blank spaces, either at the beginning 
#or at the end of the string, but also repeating spaces inside the string.

$ myVar="    kokor    iiij     ook      "
$ echo "$myVar"
    kokor    iiij     ook      
$ myVar=`echo $myVar`
$
$ # myVar is not set to "kokor iiij ook"
$ echo "$myVar"
kokor iiij ook
```

