[![Build Status](https://travis-ci.com/agamvrinos/LIICD.svg?token=xNKvEzh6d3zxdYfRyEWC&branch=master)](https://travis-ci.com/agamvrinos/LIICD)

# LIICD

This repository hosts two Python implementations of a language-agnostic Incremental Clone Detector capable of detecting Type-1 clones. Both tools have been developed in the context of a Master thesis study in collaboration with the [Software Improvement Group (SIG)](https://www.softwareimprovementgroup.com/) in the Netherlands.

## Implementations

1. The **LIICD** (under /original) implements Hummel's clone-index based approach (skipping the normalization step)
2. The **LSH-based** (under /LSH-based) utilizes Locality Sensitive Hashing (LSH) to calculate the clones for files that were found to be similar.

## Requirements

- **Python: 3.7+**
- For both sub-projects, install dependencies via `pip install requirements.txt`

## Usage 

### 1. Generate Config file
Both implementations can be run via the main script `main.py`. Before that, the generation of a configuration file indicating the commits to be analyzed, is necessary. This can be done through the `generate_config.py` script which takes a git-tracked repository and the number of commits as parameters and generates the desired file. The format of such a file looks as follows: 

```json
{
    "commits": [
        {
            "id": "cb8f645e0f",
            "changes": [
                {
                    "type": "M",
                    "filename": "lib/ansible/plugins/loader.py"
                }
            ]
        },
        {
            "id": "564907d8ac",
            "changes": [
                {
                    "type": "A",
                    "filename": "changelogs/fragments/distribution_test_refactor.yml"
                },
                {
                    "type": "R",
                    "filename": [
                        "test/units/module_utils/facts/system/distribution/__init__.py",
                        "test/units/module_utils/facts/system/__init__.py"
                    ]
                },
                {
                    "type": "D",
                    "filename": "test/units/module_utils/facts/system/distribution/fixtures/arch_linux_na.json"
                }
            ]
        }
    ]
}
```

The generated configuration file, stored under `configurations/{project_name}` must then be given as argument to the `main.py` script.

### 2. Run the Detector
The next step is to run the desired implementation, passing the required arguments. These are, the path to the repo to be analyzed, the path to the config file and the number of commits (included in that config file). 

```
python -m detector.main -p ~/projects/{my_project}/ -u ~/CloneDetector/configurations/{my_project}_updates.json -c 50
```

**Note:** Ensure that the codebase is checked-out @HEAD.

**main.py Arguments:**

- **-p**: The path to the software project to be analyzed
- **-u**: The path to the configuration file that holds the commits to be analyzed
- **-c**: The number of commits to be analyzed 

**generate_config.py Arguments:**

- **-p**: The path of the codebase for which we generate the config
- **-n**: The number of commits to analyze (default 10)

## Configuration Parameters

Both implementations include configuration parameters that allow for additional tuning. These, along with their default values, can be found in the `config.py` file of each subdirectory.

### LIICD

- **CHUNK_SIZE:** The number of lines for each consecutive block to be hashed. Consequently, defines the length of the minimum clone. (default: 6)
- **COMMITS:** The number of subsequent commits to analyze. The repository under analysis must have **at least** `COMMITS + 1` commits since the intermediate data are constructed from `HEAD-COMMITS-1`. (default: 2)
- **SKIP_DIRS:** A list of directories that are excluded from the analysis.
- **SKIP_FILES:** A list of file extensions that are excluded from the analysis.

### LSH-based

- **CHUNK_SIZE:** Identical to LIICD.
- **COMMITS:** Identical to LIICD.
- **SKIP_DIRS:** Identical to LIICD.
- **SKIP_FILES:** Identical to LIICD.
- **THRESHOLD:** The threshold of similarity based on which the files are compared. (default: 0.2)
- **PERMUTATIONS:**: The number of hash functions that are used for the generation of the MinHash signature. Affects the error rate. (default: 68)
