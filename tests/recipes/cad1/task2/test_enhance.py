"""Test the enhance module."""
# pylint: disable=import-error

from pathlib import Path

import numpy as np
import pyloudnorm as pyln
from omegaconf import DictConfig

from recipes.cad1.task2.baseline.enhance import enhance_song

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources" / "recipes" / "cad1" / "task2"


def test_enhance_song():
    """Test the enhance_song function."""
    np.random.seed(42)

    # Set the sample rate and gain
    duration = 0.5

    config = DictConfig(
        {
            "sample_rate": 16000,
            "enhance": {"min_level": -11, "max_level": -19, "average_level": -14},
        }
    )
    listener = {
        "audiogram_levels_l": [20, 30, 35, 45, 50, 60, 65, 60],
        "audiogram_levels_r": [20, 30, 35, 45, 50, 60, 65, 60],
        "audiogram_cfs": [250, 500, 1000, 2000, 3000, 4000, 6000, 8000],
    }

    # Create a sample waveform
    waveform = np.random.rand(2, int(config.sample_rate * duration))

    # Call the function
    out_left, out_right = enhance_song(waveform, listener, config)

    expected_left = np.load(
        RESOURCES / "test_enhance.enhance_song_left.npy", allow_pickle=True
    )
    expected_right = np.load(
        RESOURCES / "test_enhance.enhance_song_right.npy", allow_pickle=True
    )

    # Check that the output is not equal to the input
    np.testing.assert_array_almost_equal(out_left, expected_left)
    np.testing.assert_array_almost_equal(out_right, expected_right)

    # Check that the output has the correct loudness
    meter = pyln.Meter(config.sample_rate)

    out_loudness = meter.integrated_loudness(np.array([out_left, out_right]).T)
    assert np.isclose(out_loudness, -19, atol=0.1)
