import sys
sys.path.insert(0, '..')
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from metrics_auxiliar.run_and_extract import get_ttfaf_matrixSBF
from metrics_auxiliar.predefined_plots import plot_ttfaf, plot_cdf

DATA_FOLDER = Path(__file__).parent / 'scenarios/walk_atomium/'

sim_params = {
    "WN": 1267,
    "TOW_START": 39804,
    "TOW_STOP": 42233,
    "name": "Hot Start TTFAF - Walk in Atomium",
    "numpy_file_name": DATA_FOLDER / "ttfaf_matrix_walk_atomium.npy",
    "config_dict": {
        'scenario_path': DATA_FOLDER / 'walk_atomium_inav.sbf',
        'exec_path': DATA_FOLDER,
        'pubk_name': 'OSNMA_PublicKey.xml',
        'kroot_name': 'OSNMA_start_KROOT.txt',
        'stop_at_faf': True,
        'log_console': False,
        'log_file': False
    }
}

if __name__ == "__main__":

    options = {
        "IOD data link": {'do_crc_failed_extraction': False, 'do_tesla_key_regen': False, 'TL': 30},
        "IOD data link and Page level processing": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 30},
        "IOD data link and Page level processing - TL 29s": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 29},
        "IOD data link and Page level processing - TL 27s": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 27},
        "IOD data link and Page level processing - TL 25s": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 25},
    }

    #ttfaf_matrix = get_ttfaf_matrixSBF(sim_params, options.values(), True)
    ttfaf_matrix = np.load(sim_params["numpy_file_name"])

    plot_ttfaf(ttfaf_matrix, options.keys(), sim_params["name"])
    plot_cdf(ttfaf_matrix, options.keys(), sim_params["name"])

    plt.show()
