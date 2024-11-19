# huh: ḥuqúqu'lláh helper

Calculates 19 mit͟hqáls of gold and 19% of wealth (*after* debts and expenses); a ḥuqúqu'lláh helper.

Helps calculate the voluntary tax _Ḥuqúqu'lláh_ (_Right of God_; Arabic: _Ḥuqúq_ 'right', _Alláh_ 'God'), paid by those who have *willingly chosen* to be Bahá'í ([Wikipedia](https://en.wikipedia.org/wiki/Huq%C3%BAqu%27ll%C3%A1h); [Huqúqu'lláh Compilation](https://bahai-library.com/compilation_huququllah_right_god/)). Will retrieve the price of gold and perform the required operations, then the program will output the gold price and the payable amount of Ḥuqúqu'lláh (if any).

## Setup

### Run Program

Start program with `python -m huh` or `python app.py`.
To see options by adding `-h/--help`.

Planning to release an executable file; until then follow the instructions in [Development](#development) to get setup.

#### Configuration

Use the [`huh.ini`](./huh.ini) configuration file to change defaults (e.g., currency). File needs to be in the same directory as program or as the `app.py` file, or alternatively use `-f` to provide the `path/to/file.ini`.

**Note:** Currently does not convert amount to the default currency if prices are not available.

### Development

Clone repo, create a virtual environment, and install the necessary packages.

```bash
$ python -m venv venv
$ . venv/bin/activate # or .\venv\Scripts\Activate.ps1
$ pip install -r requirements.txt
```

Packages:

* astral
* geopy
* requests
* timezonefinder

Thank you to the respective module Authors.

## Output

In addtion to the output in terminal there is an option to store the data in CSV format if a filename is provided (`-o/--output [FILENAME]` or uncomment file under the RECORD in the config file.)

The CSV format is as follows:
`recorded date, gold price retrieved date, gold price, weight, currency, price source, wealth, payable`


## License

### [MPL-2.0](./LICENSE)

Copyright (C) 2024, Sama Rahimian. All rights reserved.

This Source Code Form is subject to the terms of the Mozilla
Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. In no world,
this or the next, shall the Author be held liable for any
damages, loss, damnation, or miscalculations, arising from the use
of this software.