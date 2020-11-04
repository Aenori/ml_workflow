import python_path

import ml_workflow
from ml_workflow.app_config import app_config
import pytest

def test_set_not_allowed():
    with pytest.raises(Exception):
        app_config.param_that_is_allowed = True

def test_set_wrong_type():
    with pytest.raises(Exception):
        app_config.df_limit_to_compress = '30'

def test_set_ok():
    app_config.df_limit_to_compress = 30
