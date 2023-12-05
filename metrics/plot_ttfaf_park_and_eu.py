import sys
sys.path.insert(0, '..')
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from osnma.input_formats.input_sbf import SBF
from metrics_auxiliar.run_and_extract import get_ttfaf_matrix
from metrics_auxiliar.predefined_plots import plot_ttfaf, plot_cdf

LOGS_PATH = Path(__file__).parent / 'metrics_live_recordings_logs/'
DATA_FOLDER = Path(__file__).parent / 'scenarios/park_and_eu/'

sim_params = {
    "WN": 1267,
    "TOW_START": 35400,
    "TOW_STOP": 37350,
    "input_module": SBF,
    "name": "Hot Start TTFAF - Park and EU District",
    "numpy_file_name": DATA_FOLDER / "ttfaf_matrix_park_and_eu.npy",
    "config_dict": {
        'logs_path': LOGS_PATH,
        'scenario_path': DATA_FOLDER / 'park_and_eu_inav.sbf',
        'exec_path': DATA_FOLDER,
        'pubk_name': 'OSNMA_PublicKey.xml',
        'kroot_name': 'OSNMA_start_KROOT.txt',
        'stop_at_faf': True,
        'log_console': False
    }
}

if __name__ == "__main__":

    options = {
        "No Optimization": {'do_crc_failed_extraction': False, 'do_tesla_key_regen': False, 'TL': 30},
        "Page level Tag processing": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': False, 'TL': 30},
        "Page level Tag processing and Key reconstruction": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 30},
        "Page level Tag processing and Key reconstruction - TL 28s": {'do_crc_failed_extraction': True, 'do_tesla_key_regen': True, 'TL': 28}
    }

    #ttfaf_matrix = get_ttfaf_matrix(sim_params, options.values(), True)
    ttfaf_matrix = np.load(sim_params["numpy_file_name"])

    plot_ttfaf(ttfaf_matrix, options.keys(), sim_params["name"])
    plot_cdf(ttfaf_matrix, options.keys(), sim_params["name"])

    plt.show()
