from pathlib import Path

import yaml


def load_options(yaml_path: str) -> dict:
    """Load options from a YAML file.

    Args:
    ----
        yaml_path (str): The path to the YAML file.

    Returns:
    -------
        dict: The loaded options as a dictionary.

    Raises:
    ------
        FileNotFoundError: If the YAML file does not exist at the path provided.
        ValueError: If the input file is not a YAML file, the YAML file is empty,
        or the 'languages' key is not a non-empty list.
    """
    if not yaml_path.endswith(".yml") and not yaml_path.endswith(".yaml"):
        msg = "The input file must be a YAML file."
        raise ValueError(msg)
    if not Path(yaml_path).exists():
        msg = f"The YAML file {yaml_path} does not exist."
        raise FileNotFoundError(msg)
    with Path.open(yaml_path) as file:
        options = yaml.safe_load(file)
        if options is None:
            msg = "The YAML file is empty."
            raise ValueError(msg)
        if (
            "languages" not in options
            or not isinstance(options["languages"], list)
            or len(options["languages"]) == 0
        ):
            msg = "The 'languages' key must be a non-empty list."
            raise ValueError(msg)
        return options
