from __future__ import annotations

import csv
import importlib
import re
from collections import defaultdict
from pathlib import Path


def generate_fixtures() -> None:
    folder_path = Path.cwd().parent / "indicator_csv_data"
    file_names = [
        f.name for f in folder_path.iterdir() if f.is_file() and f.suffix == ".csv"
    ]

    indicator_name = validate_same_indicator(file_names)
    fixture_folder = Path.cwd().parent / "fixtures" / "indicator_data"

    indicator_folder = fixture_folder / indicator_name
    indicator_folder.mkdir(parents=True, exist_ok=True)
    create_init_file(indicator_folder)

    grouped_data: dict[tuple[str, str], dict[str, list[dict[str, str | float]]]] = (
        defaultdict(dict)
    )

    for file_name in file_names:
        instrument, _indicator, buffer, params = parse_csv_file_name(file_name)
        data = load_indicator_values(Path(str(folder_path) + "/" + file_name))
        grouped_data[(instrument, params)][buffer] = data

    dump_fixtures(indicator_folder, grouped_data)

    print(f"Generated fixtures for indicator '{indicator_name}' in {fixture_folder!s}.")  # noqa: T201


def validate_same_indicator(file_names: list[str]) -> str:
    indicators = []
    for file_name in file_names:
        _, indicator, *_ = parse_csv_file_name(file_name)
        indicators.append(indicator)

    if any(indicator != indicators[0] for indicator in indicators):
        err = ""
        raise ValueError(err)

    return indicators[0]


def parse_csv_file_name(file_name: str) -> tuple[str, str, str, str]:
    instrument, indicator, buffer, params_ext = file_name.split("_", 3)
    params = params_ext.split(".")[0]
    return instrument, indicator, buffer, params


def load_indicator_values(csv_file: Path) -> list[dict]:
    indicator_values = []

    with csv_file.open() as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            indicator_values.append(  # noqa: PERF401
                {"date": row["date"], "value": float(row["value"])}
            )

    return indicator_values


def create_init_file(path: Path) -> None:
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.touch()


def dump_fixtures(
    indicator_folder: Path,
    grouped_data: dict[tuple[str, str], dict[str, list[dict[str, str | float]]]],
) -> None:
    for (instrument, params), buffers in grouped_data.items():
        file_name = f"{instrument}_{params}.py"
        module_name = file_name[:-3]  # strip .py
        file_path = indicator_folder / file_name

        lines = ["from __future__ import annotations", ""]

        for buffer, data in sorted(buffers.items()):
            _validate_buffer_dates_match(instrument, params, buffers)
            lines.append(f"{buffer} = [")
            for row in data:
                lines.append(f'    {{"date": "{row["date"]}", "value": {row["value"]}}},')  # noqa: PERF401
            lines.append("]\n")

        file_path.write_text("\n".join(lines), encoding="utf-8")

        init_path = indicator_folder / "__init__.py"
        _append_import_to_init(init_path, module_name)


def _validate_buffer_dates_match(
    instrument: str, params: str, buffers: dict[str, list[dict[str, str | float]]]
) -> None:
    buffer_dates = {
        name: [item["date"] for item in data] for name, data in buffers.items()
    }

    all_date_lists = list(buffer_dates.values())
    reference = all_date_lists[0]

    for name, dates in buffer_dates.items():
        if dates != reference:
            mismatch_info = {
                name: dates,
                "reference": reference,
            }
            msg = f"Buffer date mismatch in {instrument}_{params}: {mismatch_info}"
            raise ValueError(msg)


def _append_import_to_init(init_path: Path, module_name: str) -> None:
    indicator = init_path.parent.name

    import_lines, data_map = _read_existing_imports_and_data_map(init_path, indicator)
    _add_module_import(import_lines, data_map, indicator, module_name)
    _write_init_file(init_path, indicator, import_lines, data_map)


def _read_existing_imports_and_data_map(
    init_path: Path, indicator: str
) -> tuple[list[str], dict[str, dict[str, dict[str, str]]]]:
    import_lines = []
    data_map: dict[str, dict[str, dict[str, str]]] = {}

    if init_path.exists():
        content = init_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("import "):
                import_lines.append(line.strip())
                mod = line.strip().split()[1]
                instrument, params = mod.split("_")
                try:
                    mod_obj = importlib.import_module(
                        f"fixtures.indicator_data.{indicator}.{mod}"
                    )
                except ImportError as e:
                    msg = f"Failed to import module {mod}: {e}"
                    raise ImportError(msg)  # noqa: B904

                buffers = [k for k in dir(mod_obj) if re.fullmatch(r"b\d+", k)]
                data_map.setdefault(instrument, {})[params] = {
                    buffer: f"{mod}.{buffer}" for buffer in buffers
                }

    return import_lines, data_map


def _add_module_import(
    import_lines: list[str],
    data_map: dict[str, dict[str, dict[str, str]]],
    indicator: str,
    module_name: str,
) -> None:
    import_line = f"import {module_name}"
    if import_line not in import_lines:
        import_lines.append(import_line)
        instrument, params = module_name.split("_")
        try:
            mod_obj = importlib.import_module(
                f"fixtures.indicator_data.{indicator}.{module_name}"
            )
        except ImportError as e:
            msg = f"Failed to import module {module_name}: {e}"
            raise ImportError(msg)  # noqa: B904

        buffers = [k for k in dir(mod_obj) if re.fullmatch(r"b\d+", k)]
        data_map.setdefault(instrument, {})[params] = {
            buffer: f"{module_name}.{buffer}" for buffer in buffers
        }


def _write_init_file(
    init_path: Path,
    indicator: str,
    import_lines: list[str],
    data_map: dict[str, dict[str, dict[str, str]]],
) -> None:
    helper_lines = ["", f"{indicator}_map = {{"]
    for instrument, param_dict in sorted(data_map.items()):
        helper_lines.append(f'    "{instrument}": {{')
        for params, buffer_dict in sorted(param_dict.items()):
            helper_lines.append(f'        "{params}": {{')
            for buffer, ref in sorted(buffer_dict.items()):
                helper_lines.append(f'            "{buffer}": {ref},')
            helper_lines.append("        },")
        helper_lines.append("    },")
    helper_lines.append("}\n")

    final_code = "\n".join(import_lines + helper_lines)
    init_path.write_text(final_code + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate_fixtures()
