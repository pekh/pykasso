#!/bin/bash

docker run -ti -v $(pwd)/pykasso:/usr/src/app/pykasso -v $(pwd)/testdaten:/usr/src/app/testdaten/ pykasso pykasso $@