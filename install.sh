#!/bin/bash

printf "#!/bin/bash\n" >> ./run.sh
echo "python gui.py" >> ./run.sh

chmod 554 ./run.sh
