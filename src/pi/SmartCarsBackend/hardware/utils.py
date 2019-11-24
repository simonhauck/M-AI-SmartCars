def calculate_pollution_grade(current_pollution: float, pollution_grades: int, max_pollution: int,
                              min_pollution: int) -> int:
    """
    Calculate the relative pollution value for the given pollution
    :param current_pollution: the current absolute pollution
    :param pollution_grades: the max relative pollution
    :param max_pollution the maximum pollution where the max value will be displayed
    :param min_pollution the minimum pollution where the value will be 0
    :return: the calculate relative pollution between 0 and pollution_grades
    """

    absolute_effective_pollution = current_pollution - min_pollution

    if absolute_effective_pollution > max_pollution:
        # Max Pollution
        return pollution_grades
    elif absolute_effective_pollution <= 0:
        # Min Pollution
        return 0
    else:
        relative_effective_pollution = round(pollution_grades / max_pollution * absolute_effective_pollution)
        return relative_effective_pollution
