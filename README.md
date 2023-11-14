[![ICD Test Vectors](https://github.com/Algafix/OSNMA/actions/workflows/icd_test_vectors.yml/badge.svg)](https://github.com/Algafix/OSNMA/actions/workflows/icd_test_vectors.yml)
[![Python 3.8](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_38.yml/badge.svg)](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_38.yml)
[![Python 3.9](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_39.yml/badge.svg)](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_39.yml)
[![Python 3.10](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_310.yml/badge.svg)](https://github.com/Algafix/OSNMA/actions/workflows/tests_python_310.yml)

OSNMAlib
========

OSNMAlib is an open-source Python library that can be integrated into existing receivers and applications to incorporate 
navigation message authentication to the positioning process. It can read the Galileo I/NAV pages when received, store 
the navigation and authentication data, perform the authentication verification, and report the status.

The software has been succesfully tested using the official ICD test vectors from the [Receiver Guidelines for the Test Phase v1.1](https://www.gsc-europa.eu/sites/default/files/sites/all/files/Galileo_OSNMA_Receiver_Guidelines_for_the_Test_Phase_v1.1.pdf) available [here](https://www.gsc-europa.eu/sites/default/files/sites/all/files/osnma_annex_2.zip). It has also been tested with old test vectors and real live data recorded by me.

Supports Python 3.8, 3.9 and 3.10+. Tested on Linux and Windows.

**NOTE:** If you want to use live data after 2023-08-03 11:00, please checkout the [ICD 1.0 branch](https://github.com/Algafix/OSNMA/tree/OSNMA_ICD_1.0/)

Features
---

Current OSNMA ICD **features supported**:

  * Verification of the public key retrieved from the DSM-PKR message.
  * Verification of the TESLA root key retrieved from the DSM-KROOT message (all algorithms).
  * Verification of a TESLA key against a root key or a previously authenticated key.
  * Verification of the MACK message structure:
    * ADKD sequence.
    * MACSEQ value.
    * FLX tags.
  * Verification of the ADKD 0, ADKD 4 and ADKD 12 tags.
  * Authentication of the navigation data.
  * Support for Cold Start, Warm Start and Hot Start.
  * Support for the following events: EOC, NPK, PKREV, OAM.
    * Missing data to validate the CREV event.
  
**Extra optimizations** for a faster TTFAF:
  * Reconstruct broken HKROOT messages.
  * Reconstruct TESLA key from partial MACK messages.
  * Extract non-FLX tags from broken MACK messages.

Current data **format supported**:

  * Septentrio Binary Format (SBF) log files.
  * Live connection to a Septentrio Receiver through IP port.
  * Live aggregated data from the [galmon](https://github.com/berthubert/galmon) project.
  * Allows for custom data by implementing your iterator.

Future development:

  * **Done!** ~~Support for SBF directly (no conversion to SBF Ascii).~~
  * **Done!** ~~Development of an input iterator for real-time navigation data.~~
    * ~~Integration with SBF logging real-time navigation data.~~
    * ~~Integration with Galmon real-time navigation data.~~
  * **Done!** ~~Reconstruct MACK subframes.~~
  * **Done!** ~~TTFAF metric displayed in the logs.~~
  * Time synchronization options.
  * Clean up the new ICD 1.0 branch, and implement COP.
  * Rework of the data link module.

Documentation
---

NAVITEC Conference on OSNMAlib
  * [OSNMAlib Paper](OSNMAlib_NAVITEC2022.pdf)
  * [Youtube Presentation](https://www.youtube.com/watch?v=IVPzVM5GdKs)

General OSNMA documentation
  * [GSC website with the reference documents](https://www.gsc-europa.eu/electronic-library/programme-reference-documents)
  * Look both at the ICD and the Receiver Guidelines
 

Quick Run - Try it!
===

Requirements
---

The required Python libraries can all be installed with `pip` using the `requirements.txt` file.

```
$ pip install -r requirements.txt
```

Current configuration
---

**NOTE:** If you want to use live data after 2023-08-03 11:00, please checkout the [ICD 1.0 branch](https://github.com/Algafix/OSNMA/tree/OSNMA_ICD_1.0/)

The folder `custom_run/` contains the current Merkle Tree and Public Key, both downloaded from the official [GSC](https://www.gsc-europa.eu/) website. It also contains the `current_config.sbf` file with the current configuration recorded by me. You can run it directly with the console with:

```
$ cd custom_run/
$ python run.py
```

**Beware** the console output will be huge, you can limit it in the configuration dictionary. A log folder will be created with the same logs for easy parsing.

You can also run your own SBF files (if they contain the GALRawINAV block) by giving it the same name or passing the file as parameter. Mind to also update the Merkle Tree and Public Key files accordingly.

```
$ cd custom_run/
$ python run.py [filename]
```

Real time execution with data from Galmon
---

**NOTE:** Please checkout the [ICD 1.0 branch](https://github.com/Algafix/OSNMA/tree/OSNMA_ICD_1.0/) to use galmon with the new ICD live data.

If you want to see the library process data in real time but don't have a receiver, I've integrated OSNMAlib with the [galmon](https://github.com/berthubert/galmon) project. You can find a  under the folder `live_galmon_run/` and run it:

```
$ live_galmon_run/
$ python run.py
```

You will see information printed about every 30s approximately.
There may be some problems with the data received from galmon due to the P2P nature of this service.

The IP and Port are defaulted to `86.82.68.237:10000`. You can specify your own in the Galmon input class constructor.

Real time execution with a Septentrio receiver
---

If you have access to a Septentrio receiver SBF log output, I have implemented a real time input module for that. To tell the receiver to output the required navigation data send the following commands to it. Mind that `Stream2` or port `20000` may be in use. 

```
setSBFOutput, Stream2, IPS1, GALRawINAV, sec1
setIPServerSettings, IPS1, 20000
```

Then just execute the software. By default it connects to `192.168.3.1:20000`.

```
$ live_septentrio_run/
$ python run.py
```

Custom data format
---

If you want to use a different data format, go to [Execution with Custom Data](#execution-with-custom-data). 

Test Execution
===

The software is provided with several test scenarios under the folder `tests/scenarios/`. The scenarios cover 
different configurations and events of the OSNMA protocol. The data used by this tests was recorded on the OSNMA 
Internal and Public Test Phases (2020 - 2022).

To run the test is recommended to use the Python framework `pytest`, although they can be run calling the traditional 
Python interpreter. Keep in mind that this execution may take a few minutes, since each test comprises several hours of satellite data.

By default, all tests are executed with `info` logging level on the file handler. That is, the log files will
contain the maximum amount of information. This log files are stored under the folder `tests/test_logs`.
For each sub-test (in this case, for each scenario) a subfolder is created with the name format `logs_YYYYmmdd_HHMMSS`.

Pytest
---

The `pytest` framework is the easiest way to execute the OSNMA Open Implementation receiver tests. To do so, the 
following shell commands are provided. Note that the users interpreter work directory is assumed to be the top
folder of the provided software and `python pip` shall be already installed.

```
$ pip install -r requirements.txt
$ cd tests
$ pytest receiver_test.py
```

Python interpreter
---

The tests can also be executed using the traditional Python interpreter. In that case, the following shell commands 
should be executed.

```
$ pip install -r requirements.txt
$ cd tests
$ python3 receiver_test.py
```

Execution with Custom Data
===

The OSNMA Open Implementation receiver can be used with custom data files. However, the receiver is only guaranteed to 
work with data consistent with the OSNMA User ICD for the Test Phase version 1.0.

Septentrio Binary Format (SBF)
---

If the custom navigation data is available in Septentrio Binary Format (SBF), the receiver already includes the input 
iterator `SBF` to handle it. The SBF file used needs to contain the block with the raw Galileo INAV bits (GALRawINAV)
so OSNMAlib can process them.

We are also including the iterator `SBFAscii` for the cases where the GALRawINAV
data is in SBF ascii mode (converted from an SBF file using the official tools).

Both can be found [here](https://github.com/Algafix/OSNMA/blob/master/osnma/input_formats/input_sbf.py).

Custom format
---

If the format of the custom data is not supported by OSNMAlib, a new input iterator should be developed following
the instructions on the [Input Data wiki page](https://github.com/Algafix/OSNMA/wiki/Input-Data).


Receiver Options
---

The receiver has several configuration parameters that should be defined previous to execution. Those parameters can be 
specified within code in a Python dictionary or in a separate JSON File and served as an input parameter to the 
receiver. The receiver will load default values for the configuration parameters not specified.

The most important parameters are:

* `scenario_path`: Path to the scenario data file.
* `exec_path`: Path to the folder where the receiver will search for the Merkle Tree root, Public Key and KROOT files, and where will store the keys and the logs (if no log path is specified).
* `merkle_name`: Name of the Merkle Tree root file. Shall be in the GSA XML format.
* `pubkey_name`: Name of the stored Public Key file. Shall be in the GSA XML format.

For a full description see the wiki page [Receiver Options [TBC]](https://github.com/Algafix/OSNMA/wiki/Receiver-Options-%5BTBC%5D).


Research Notice
===

This repository partially contains data, information and ideas regarding an ongoing PhD research.

Please don't publish your own results based on OSNMA ideas and optimizations read on this repository until they have been scientifically disclosed. I will update this note once that happens.

I strongly believe in open-source software and free access to knowledge, and this whole project remains open to honour these ideals.

However, this approach by my side requires the uttermost respect to the research integrity and ethics by anyone accessing this repository. 

In case of doubt, contact me at algafix[@]protonmail.com

Thank you.


Support
===

If you are having issues, please use the Issues page in GitHub.

Contribution
===

If you want a protocol to be supported as an input for OSNMAlib you can kindly request it in the GitHub Issues page, providing its documentation and possible ways to test it.

Or you can create a Pull Request with your implementation. I will help you with any question that you may have about the interface class.

License
===

The project is licensed under the EUPL.

About
===

The research leading to this work has been supported by European Commission contract SI2.823546/9 and by the Spanish Ministry of Science and Innovation project PID2020-118984GB-I00. 

Disclaimer
===

OSNMAlib has not been developed or tested operationally. OSNMAlib users use it at their own risk, without any guarantee or liability from the code authors or the Galileo OSNMA signal provider.

OSNMAlib is not affiliated with any private company.
